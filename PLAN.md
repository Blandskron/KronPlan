# Trabajo Pendiente

## Fase 2 — Branding y Design System (KronPlan)

Siguiente unidad de trabajo planificada en [`ROADMAP.md`](ROADMAP.md) (Fase 2, etapas 2.1 a 2.3):

1. Documentar la identidad visual y tokens en `docs/BRAND_GUIDELINES.md` y `docs/DESIGN_SYSTEM.md`.
2. Crear los activos vectoriales originales en `static/brand/` (isotipo K + cartas, logos dark/light, variantes monocromáticas, favicon SVG y tarjeta social OG).
3. Migrar las primitivas de `static/css/style.css` al sistema `--kp-*` (Dark Mode por defecto, Light Mode y preferencia del sistema, tipografías Sora / Inter / JetBrains Mono, escala de 4 px, radios 8/12/16/24 px, Lucide SVG y sprites vectoriales actualizados) manteniendo 0 fallos WCAG 2.2 AA.

## Cobertura del consumer

`rooms/consumers.py` está al **78 %**, por debajo del resto (`services.py` al 96 %). El
umbral general de CI es 80 % y la suite está en 85,62 %.

Lo que no está cubierto, en orden de importancia:

1. **Caminos de error del despacho.** Payload inválido, `event_type` desconocido, y una acción
   de facilitador enviada por alguien que no lo es. Debe responder un `error` estructurado
   sólo al socket que lo pidió, y no tocar a nadie más de la sala.
2. **Ciclo de conexión con varias pestañas.** `participant.joined` se emite en la primera
   pestaña y `participant.left` en la última que se cierra. `connection_count` es el contador
   que lo decide y sus bordes no tienen test.
3. **`player.moved`.** El descarte silencioso por debajo de los 110 ms y el rechazo cuando el
   recreo está cerrado.

## Test de tiempo real contra Redis real

El `socket_timeout` (`REDIS_SOCKET_TIMEOUT`, 20 s por defecto) ya está aplicado en
`config/settings.py` y verificado estructuralmente en `rooms/test_channel_layer.py`. Lo que
sigue pendiente de Fase 4 es un test de integración reproducible contra un Redis real que abra un
socket y espere más de 6 s para asegurar que un salto de versión no reabra el `TimeoutError` en
silencio.

## La barra inferior también dentro de la sala

El rediseño móvil dejó la barra de pestañas fuera de la sala, porque el borde inferior lo ocupa
la baraja. La sala es justo donde más se nota que no hay navegación.

**Decidido:** las dos capas se apilan, como en las apps con reproductor. La barra de pestañas se
queda fija en el borde y la mano se apoya encima de ella. Cuesta unos 60 px de mesa y votar sigue
siendo un solo toque, que es lo que no se puede perder.

Consecuencias concretas: `body.is-room .app-tabbar { display: none }` desaparece; la mano se
ancla en `bottom: var(--tabbar-height)` en vez de en `0`; el relleno inferior de `.room-shell`
pasa a ser la suma de las dos alturas, y `--deck-dock-height` se sigue midiendo —no se suma a
ojo—. El test `test_the_hand_is_docked_to_the_bottom_edge_of_a_phone` afirma hoy que la barra
**no** está visible en la sala: hay que darle la vuelta, no borrarlo.
