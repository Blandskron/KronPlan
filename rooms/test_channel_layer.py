"""La capa de canales con Redis real, que es la única que corre en producción.

La suite entera usa `InMemoryChannelLayer`, así que todo lo que dependa de cómo se
configura Redis es invisible para ella. Eso ya costó caro una vez: `channels_redis`
espera mensajes con un bloqueo de 5 s y no le pasa ningún tiempo de lectura a
redis-py; redis-py 8.x aplicaba entonces uno sin holgura, el cliente abandonaba justo
antes de que contestara el servidor, y cada WebSocket moría a los ~6 s. La sala en
producción reconectaba en bucle mientras los 126 tests seguían en verde.

Este test no necesita un Redis levantado: comprueba la invariante estructural que
mantiene sana esa conversación, que es lo que se rompió.
"""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from channels_redis.core import RedisChannelLayer

BASE_DIR = Path(__file__).resolve().parent.parent


def channel_layers_with(redis_url):
    """Carga `config.settings` en un proceso limpio con REDIS_URL puesto.

    En proceso no vale: `CHANNEL_LAYERS` se calcula al importar, y recargar el módulo
    debajo de una instancia de Django ya arrancada tiene más efectos que el que se
    quiere medir.
    """
    code = (
        "import os, json; os.environ['REDIS_URL'] = %r;\n"
        "os.environ.setdefault('DJANGO_SECRET_KEY', 'x' * 50);\n"
        "import django; os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings';\n"
        "from django.conf import settings; print(json.dumps(settings.CHANNEL_LAYERS))"
    ) % redis_url
    result = subprocess.run(
        [sys.executable, "-c", code], cwd=BASE_DIR, capture_output=True, text=True, timeout=120
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout.strip().splitlines()[-1])


@pytest.fixture(scope="module")
def redis_layer():
    return channel_layers_with("redis://localhost:6379/0")["default"]


def test_redis_is_used_when_a_url_is_configured(redis_layer):
    assert redis_layer["BACKEND"] == "channels_redis.core.RedisChannelLayer"


def test_the_read_timeout_leaves_room_for_the_blocking_pop(redis_layer):
    """La invariante: el tiempo de lectura tiene que superar al del bloqueo.

    Si alguien quita `socket_timeout`, o lo deja por debajo de `brpop_timeout`, el
    cliente volverá a abandonar antes de que el servidor conteste y la sala volverá a
    reconectar en bucle, sin que ningún otro test se entere.
    """
    host = redis_layer["CONFIG"]["hosts"][0]
    assert isinstance(host, dict), (
        "los hosts volvieron a ser una URL suelta: así no se puede pasar socket_timeout"
    )
    assert "socket_timeout" in host, "sin socket_timeout, cada WebSocket muere a los ~6 s"
    assert host["socket_timeout"] > RedisChannelLayer.brpop_timeout, (
        f"socket_timeout={host['socket_timeout']} no deja holgura sobre el bloqueo de "
        f"{RedisChannelLayer.brpop_timeout}s de channels_redis"
    )


def test_without_a_redis_url_the_layer_stays_in_memory():
    """Es lo que usa la suite y el desarrollo local; no debe arrastrar Redis."""
    layer = channel_layers_with("")["default"]
    assert layer["BACKEND"] == "channels.layers.InMemoryChannelLayer"


@pytest.mark.asyncio
async def test_live_redis_channel_layer_survives_past_blocking_pop_timeout():
    """Contra un Redis real, esperar más de 6 s no debe lanzar redis TimeoutError."""
    redis_url = os.environ.get("REDIS_LIVE_URL")
    if not redis_url:
        pytest.skip("REDIS_LIVE_URL no definido; se omite prueba contra Redis real.")

    layer = RedisChannelLayer(
        hosts=[{"address": redis_url, "socket_timeout": 20, "socket_connect_timeout": 5}]
    )
    try:
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(layer.receive("kronplan.test.idle.channel"), timeout=6.5)
    finally:
        await layer.close_pools()
