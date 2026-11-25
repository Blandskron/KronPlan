# Registro de Decisiones Arquitectónicas (ADR)

Este documento registra decisiones técnicas y de diseño importantes que impactan a Planning Pocket.

---

## ADR-001 — Django como framework central

**Estado:** Aceptado

**Decisión:** Utilizar Python con Django como el entorno principal para construir el producto, y renderizar el frontend inicial con Django Templates. No crear una SPA de inmediato.

**Motivo:** Queremos mantener el proyecto simple, rápido de iterar y reducir la complejidad del ciclo de CI/CD. Django nos proporciona autenticación, ORM seguro, sesiones de manera inmediata, eliminando la fricción de manejar CORS, tokens JWT y APIs REST para operaciones triviales iniciales.

**Consecuencias:**
- La experiencia inicial podría parecer tradicional, pero se compensará con interactividad incremental (WebSockets/HTMX).
- Mayor dependencia en la redención de plantillas en el servidor.

---

## ADR-002 — Django Channels y Redis para tiempo real

**Estado:** Aceptado

**Decisión:** Adoptar WebSockets mediante Django Channels y usar Redis como capa base.

**Motivo:** Una aplicación de Planning Poker pierde su utilidad si la mesa requiere F5/recargar para ver los votos de los demás. Requerimos notificaciones push desde el backend a todos los clientes de una sala concurrentemente con latencia baja.

**Consecuencias:**
- Requiere correr ASGI (como Daphane o Uvicorn) en lugar del tradicional WSGI en producción.
- Añade Redis a la matriz de dependencias e infraestructura.

---

## ADR-003 — Autoridad en el Servidor (Server-Side Authority)

**Estado:** Aceptado

**Decisión:** El frontend carece totalmente de poder sobre las validaciones, el estado de la ronda, y los cálculos estadísticos.

**Motivo:** Al existir roles (Facilitador, Invitado) y reglas estrictas de privacidad antes del *reveal*, la arquitectura no puede confiar en el lado del cliente (Navegador) para ocultar información, porque es fácilmente auditable o manipulable.

**Consecuencias:**
- Todo evento generado por el usuario ("Votar") es solo una "intención" que el Servidor debe ejecutar.
- El servidor deberá enviar estados consolidados por WebSockets a los clientes.

---

## ADR-004 — URL Compartida con Identificador Impredecible

**Estado:** Aceptado

**Decisión:** Las URL para unirse como invitado se basarán en un identificador alfanumérico aleatorio (ej. `public_id`).

**Motivo:** Facilitar el acceso rápido al equipo sin cuentas, y prevenir enumeración y robo de privacidad si se usaran identificadores numéricos incrementales.

---

## ADR-005 — Capa de juego cosmética y autoritativa en el servidor

**Estado:** Aceptado

**Decisión:** Añadir una capa de interacción entre pares — lanzar objetos blandos a
otra persona de la mesa — que es puramente cosmética, efímera y desactivable por dos
interruptores independientes. El servidor decide cada lanzamiento; el navegador sólo
envía una intención y espera el broadcast.

**Motivo:** La sala funcionaba pero se sentía como un formulario. La espera entre el
primer voto y el último es tiempo muerto, y es justo donde un equipo que está en la
misma sala bromearía. Queremos recuperar ese momento sin convertirlo en presión.

Esto **revierte una decisión anterior de producto**: `docs/ROOM_VISUAL_DESIGN.md`
traducía «atacar» como un recordatorio amable, exclusivo del facilitador. El
recordatorio se conserva, pero deja de ser la única interacción posible entre
personas.

**Consecuencias:**

- Dos eventos nuevos en el protocolo: la acción `player.throw {target_id, item}` y el
  evento `player.hit {thrower_id, target_id, item}`. El payload se comprueba con
  igualdad exacta en los tests: es todo el contrato, y no cabe nada más.
- Tres campos nuevos: `PokerRoom.allow_playful_actions`,
  `Participant.last_throw_at` y `Participant.throws_this_round`.
- Los límites viven en `rooms/services.py`, no en el cliente: 2,5 s de espera por
  persona y un tope por ronda. El navegador no puede concederse un brazo más rápido.

**Reglas que hacen que esto siga siendo un juego.** Son parte de la decisión, no una
nota al pie:

1. **El voto sigue privado.** Ni `player.throw` ni `player.hit` transportan
   información de voto, y hay un test que lo verifica con igualdad exacta del payload.
2. **El objeto es idéntico haya votado el destinatario o no.** Las comprobaciones del
   servicio son deliberadamente ciegas a `current_vote`, así que un lanzamiento nunca
   puede leerse como una señal sobre la carta de alguien ni sobre su silencio.
3. **Nada acumula.** `throws_this_round` muere con la ronda. No hay marcador de quién
   recibió más impactos ni ranking de quién tardó más.
4. **Nada automático ni dirigido por estado.** Ningún objeto sale solo hacia quien no
   ha votado, y el aro de puntería aparece igual sobre todas las caras.
5. **El catálogo se queda blando.** Comida, papel y objetos de oficina absurdos.
   Ningún objeto que lea como arma o como daño.
6. **Doble consentimiento.** El facilitador apaga la capa para toda la sala;
   cada persona puede apagar los efectos en su propia pantalla. Y
   `prefers-reduced-motion` manda por encima de ambos.
7. **La reunión gana.** Nada tapa la mano de cartas ni el botón de revelar, nada
   bloquea la entrada, y los proyectiles y las manchas del paño tienen tope.

**Alternativa descartada:** dejar el «ataque» sólo como recordatorio del facilitador.
Es más seguro, pero mantiene la asimetría que hacía que la sala se sintiera como un
panel de administración: una persona con controles y el resto esperando.

---

## ADR-006 — Capa de tokens semánticos y carcasa de aplicación en móvil

**Estado:** Aceptado (evolucionado hacia el sistema KronPlan en ADR-009)

**Decisión:** Desacoplar los componentes visuales mediante una capa de tokens semánticos
(`--surface`, `--accent`, `--felt`, `--radius-*`…) y hacer que por debajo de 821px la interfaz
se comporte como una aplicación móvil en lugar de como una página web estrecha.

**Motivo.** El sistema visual inicial —paño plano y acento terracota— requería una capa
moderna unificada con temas claro/oscuro y tokens reutilizables sin reescribir la geometría
de la mesa. En móvil, además, había un agujero real: a partir de 700px los enlaces del
encabezado se ocultaban por falta de sitio y no reaparecían en ningún otro lugar, así que desde
un teléfono no se podía crear una sala ni cerrar sesión.

**Cómo se implementa.** Los valores de marca se declaran una sola vez en la raíz de
`static/css/style.css` y se traducen a los nombres semánticos que consumen los componentes
(`--surface`, `--accent`, `--felt`, `--radius-*`…). Ningún componente lee una primitiva
directamente. Esto permite cambiar o evolucionar la marca tocando únicamente el bloque de
tokens, sin tocar la geometría de la mesa verificada al píxel por los tests de navegador.

**Consecuencias:**

- El acento decorativo (`--brand`) y el interactivo (`--accent`) se separan en tokens distintos:
  `--brand` decora y nunca lleva texto; `--accent` es el interactivo calibrado para superar
  4,5:1 (AA) en claro y en oscuro. Quien cambie uno por el otro rompe el contraste sin verlo.
- **Una superficie que no cambia con el tema no puede llevar texto de un token que sí cambia.**
  Esto no se dedujo: se encontró midiendo. La cara de la carta es clara en los dos temas y
  `.participant-front.no-vote` usaba `--muted`, que en oscuro es blanco: al revelar, el guion de
  «no votó» quedaba en 1,08:1, invisible. Lo mismo con el rótulo sobre el panel oscuro de marca
  (`--brand-bright`, 4,1:1). Las tres superficies fijas —cara de carta, panel de marca y paño—
  derivan su tinta de sí mismas, nunca del tema. Ver `docs/PRODUCT.md`.
- El paño de la mesa se mantiene oscuro en ambos temas. Los asientos siempre caen sobre él, así
  que la paleta de asientos tampoco cambia con el tema.
- Las fuentes se cargan desde Google Fonts con la familia del sistema como respaldo. Si no
  cargan, el texto se dibuja con la pila de respaldo y nada se descoloca.
- El tema oscuro es la lectura canónica del producto. El claro se mantiene, y la preferencia del
  usuario sigue mandando sobre la del sistema.
- En móvil aparecen dos elementos anclados que antes no existían —la barra de pestañas y la
  baraja— y ninguno puede tapar lo que hay debajo. La altura de la baraja se **mide** y se
  publica en `--deck-dock-height`, en lugar de reservar un hueco fijo que sobraría o faltaría
  según la bandeja de objetos esté abierta o no.

**Alternativa descartada:** acoplar los componentes directamente a colores fijos en cada regla
CSS, lo que multiplica el coste de cualquier cambio futuro de identidad o tema.

---

## ADR-007 — Moderación de la sala: dos barajas y expulsión con veto

**Estado:** Aceptado

**Decisión:** El facilitador gana dos poderes sobre la sala. Primero, la baraja por
defecto pasa a ser de ocho cartas (`0 1 2 3 5 8 13 ?`) y un interruptor la lleva a las
trece de siempre. Segundo, puede expulsar a un participante, y la expulsión **veta**:
esa persona no vuelve a entrar con el mismo enlace.

**Motivo.** Trece cartas en un teléfono se recorren de lado, y las cuatro últimas de
Fibonacci sirven para discutir una vez al trimestre. Y una sala que se comparte por un
enlace impredecible pero público necesita que quien la abre pueda cerrarle la puerta a
alguien, por el motivo que sea: un nombre que no corresponde, una pestaña zombi, una
persona que no debería estar.

**Cómo se implementa, y lo que no es obvio:**

- **Dos listas cerradas, no una baraja configurable.** Viven en `rooms/decks.py`, como
  las mascotas viven en `identity.py`. Una baraja escrita a mano obliga a validar
  longitud, duplicados y qué cuenta como numérico para el promedio, a cambio de una
  libertad que nadie pidió. `is_expanded()` se deriva de lo guardado en lugar de llevar
  un booleano aparte, para que no puedan contradecirse.
- **Al encoger, los votos huérfanos se retiran.** Un voto de una carta que ya no está
  en la mesa aparecería al revelar como un 55 que no se puede volver a elegir, y el
  promedio lo contaría: un número que nadie puede reproducir. El evento lleva a quién
  le pasó, para que lo vea en el momento y no al final.
- **La baraja no cambia bajo una ronda revelada**, igual que el recreo no se abre con
  las cartas sobre la mesa. Cambiarla ahí reescribe un resultado que se está discutiendo.
- **La expulsión no borra la fila: la fila *es* el veto.** `Participant.removed_at`
  marca la salida y el registro se queda, porque guarda el `guest_token` —o el usuario—
  con el que esa persona volvería a entrar. Borrarla dejaría que volviese con el mismo
  enlace diez segundos después, que es exactamente no haber expulsado a nadie.
- Por eso aparece `PokerRoom.active_participants`: **cualquier sitio que dibuje, cuente
  o promedie la mesa tiene que pasar por ahí**, y `_get_seated()` protege cada acción
  sobre un participante. Sin esa segunda guarda, el socket que el expulsado ya tenía
  abierto seguiría votando.
- El veto se comprueba en los dos sitios por los que se entra: la vista HTTP —el
  cliente recarga la página en cuanto se le cierra el socket— y `get_participant()` del
  consumer, porque reconectar es lo primero que hace el cliente al caerse.

**Límite conocido, y es real:** un invitado expulsado que vacíe las cookies del
navegador puede volver a entrar como alguien nuevo. La identidad de un invitado es su
`guest_token` y no hay nada más fuerte que vetar sin pedir una cuenta. Para un
participante autenticado el veto es contra el usuario y sí es firme. No lo tapamos con
IP: castigaría a toda una oficina detrás del mismo NAT.

**Alternativa descartada:** una expulsión blanda, que sólo saca de la mesa y deja
volver. Es mucho más simple —no hay nada que persistir— pero sirve para limpiar un
nombre mal escrito, no para apartar a alguien, que es lo que se pidió.

---

## ADR-008 — Endurecimiento tras la revisión de seguridad

**Estado:** Aceptado

**Decisión:** Cerrar los huecos que encontró una revisión completa del código. No es una
funcionalidad nueva: es la diferencia entre un modelo de autorización correcto sobre el
papel y uno que también lo es cuando alguien empuja.

**Los tres que importan, y por qué no se veían:**

1. **Sin límite en lo que escribe.** Las acciones decorativas tenían freno —lanzar espera
   2,5 s, moverse 110 ms— y votar no tenía ninguno. Medido contra el contenedor: 300
   `vote.cast` seguidos, cero errores, reparto completo. Cada uno es un `SELECT FOR
   UPDATE` sobre la sala más N frames. Y como la sala no tenía tope, N lo elegía el
   atacante. Ahora hay ventana deslizante por conexión y `MAX_PARTICIPANTS`.

2. **La sesión no alcanzaba a los sockets abiertos.** `AuthMiddlewareStack` resuelve
   `scope["user"]` una vez, al conectar, y ahí leían todas las comprobaciones de
   facilitador. Cerrar sesión no le quitaba el control de la sala a nadie hasta que
   cerrase la pestaña. `live_actor()` relee la sesión en cada acción de facilitador.

   Esto obligó a cambiar el banco de pruebas: los tests de WebSocket autenticaban
   poniendo `scope["user"]` a mano, que es algo que producción nunca hace. Ahora crean
   una sesión real. Un banco que se salta la sesión no prueba el camino que importa.

3. **Sin CSP.** Mil líneas de JavaScript en línea, manejadores `onclick` incrustados y un
   `innerHTML` alimentado con el nombre que escribe un invitado. Ese `innerHTML` se
   defendía borrando comillas dobles y **no llegaba a ser explotable** —verificado en
   navegador con cuatro payloads, cero ejecuciones— pero era una lista negra en un sink
   de HTML. Ahora se construye nodo a nodo, los `onclick` son listeners delegados, y la
   política con nonce impide que un script inyectado corra aunque entre.

**Lo demás, en una línea cada uno:**

- `player.move` era la única acción que no pasa por `rooms/services.py`, y por tanto la
  única sin `_require_active_room`: se podía pasear por una sala cerrada. Ahora el cierre
  cierra el recreo y avisa por el canal, de modo que cerrar una sala alcanza a quien ya
  está dentro en vez de ser sólo una fila en la base.
- Fuerza bruta: `accounts/throttling.py`, contando por usuario y no por IP, porque detrás
  de un proxy contar por IP es confiar en una cabecera falsificable o castigar a toda una
  oficina.
- Nadie podía saber quién era el facilitador: la insignia existía sólo en su propia barra.
  `is_facilitator` viaja ahora en el estado del participante.
- `PokerRoom.reset_voting()` era código muerto **y además saltaba la autorización**: quien
  lo llamara reiniciaba la ronda sin pasar por `_require_facilitator`. Borrado.
- `config/asgi.py` creaba el superusuario en tiempo de importación, con un `except
  Exception` mudo, duplicando lo que ya hacen el entrypoint y `build.sh`. Borrado.
- Una 404 devolvía `{"error": "Not found"}` en JSON. El producto entero entra por un
  enlace compartido, así que teclear mal el enlace es el error más probable que existe.
- `LANGUAGE_CODE` era `en-us` en un producto en español, y no había `LOGGING`: los 500
  iban a `mail_admins` sin `ADMINS`, o sea a ninguna parte. Así vivió el fallo de Redis.

**Un hallazgo de la revisión resultó ser falso**, y conviene dejarlo escrito para que nadie
lo "arregle": el bloque `MAILERS` de `settings.py` parece configuración muerta porque no
aparece en `django.conf.global_settings`. No lo es. `MAILERS` es la API de correo de
Django 6.1 y `EMAIL_BACKEND` está deprecado, retirado en 7.0; definir los dos a la vez es
un error de configuración. El código estaba bien.

**Concesión explícita:** `style-src` admite `'unsafe-inline'`. La mesa coloca cada asiento
escribiendo `style="--seat-angle: …"`, y un atributo de estilo no se puede firmar con
nonce. Quitarlo exigiría mover la geometría del anillo a clases, que es precisamente lo
que el ADR anterior evitó para no tocar una geometría verificada al píxel.

---

## ADR-009 — Evolución a KronPlan (ecosistema BLANDSKRON) e incorporación de skills de diseño

**Estado:** Aceptado

**Contexto:** Planning Pocket pasa a denominarse oficialmente **KronPlan — Agile Planning & Estimation** (*Plan together. Build better.* · *Open Source · By BLANDSKRON*), integrándose en el ecosistema open source de BLANDSKRON (`blandskron.cl` / `Blandskron/blandskronSPA`). La paleta heredada previa (rosa `#ed117b` sobre azul `#202b70`, tipografía Manrope + Inter) no reflejaba la identidad propia del ecosistema KRON ni de BLANDSKRON (violeta/índigo/cian sobre obsidiana, con `JetBrains Mono` como sello técnico).

**Decisión:**

1. **Identidad y sistema de diseño KronPlan (`--kp-*`):** Reemplazar la paleta heredada por un sistema de diseño original para KronPlan alineado con el ADN de BLANDSKRON:
   - Colores de marca: Agile Violet `#A78BFA`, Planning Purple `#7C3AED`, Collaboration Indigo `#6366F1`, Velocity Cyan `#22D3EE` y Soft Lavender `#DDD6FE`, sobre neutros oscuros (`#0D1020`, `#17182D`, `#211F38`, `#34314D`) y superficie clara (`#F5F7FB`).
   - Tipografías: **Sora** (display/títulos), **Inter** (interfaz/cuerpo) y **JetBrains Mono** (cartas, códigos de sala y cifras tabulares), con respaldo del sistema.
   - Forma y movimiento: escala base de 4 px, radios de 8/12/16/24 px (manteniendo píldoras en acciones clave donde convenga), iconografía Lucide SVG, microinteracciones de 150–250 ms y respeto estricto de `prefers-reduced-motion`.
   - **Tema de 3 estados:** `dark` como lectura canónica por defecto, `light` y `system`, con lectura retrocompatible de preferencias almacenadas previamente bajo `planning-pocket-*`.
2. **Ajustes obligatorios tras revalidación WCAG 2.2 AA:**
   - `#7C3AED` no alcanza 4,5:1 como texto sobre fondos oscuros (`2,80–3,31:1`), por lo que se reserva para fondos de botón primario con texto `#FFFFFF` (`5,70:1`), bordes e íconos; el texto interactivo en oscuro usa `#A78BFA` (`5,86–6,94:1`).
   - `#EF4444` cae a `4,23:1` sobre `#211F38`: el texto de error sobre superficies oscuras elevadas usa `#F87171` y en modo claro `#DC2626` (`4,50–4,83:1`).
   - `#64748B` cae por debajo de `4,5:1` en texto normal tanto en oscuro (`3,35–3,97:1`) como en `#F5F7FB` (`4,44:1`): los textos inactivos usan `#94A3B8` en oscuro y `#475569` en claro, conservando `#64748B` para puntos/bordes.
   - En modo claro, los acentos y semánticos de texto se mapean a variantes profundas verificadas AA (`#6D28D9`, `#4F46E5`, `#0E7490`, `#15803D`, `#B45309`, `#DC2626`, `#0369A1`, `#0F766E`), manteniendo la invariante de las tres superficies fijas de ADR-006 (cara de la carta, panel de marca oscuro y paño de la mesa).
3. **Arquitectura nativa conservada:** Todo el frontend se consolida con Django Templates, HTML, CSS y Vanilla JS + WebSockets (ADR-001, ADR-002, ADR-003). No se introducen frameworks SPA ni dependencias de build en runtime. Se preservan todos los modelos, rutas (`/p/<public_id>/`), contratos WebSocket, CSP con *nonce* y garantías de privacidad de votos pre-reveal.
4. **Incorporación auditada de la skill `ui-ux-pro-max`:** Se incorpora en `.agents/skills/ui-ux-pro-max/` (fijada al commit `8db36338810d` de `nextlevelbuilder/ui-ux-pro-max-skill`, licencia MIT) tras auditar que sus 6 scripts Python usan solo biblioteca estándar, operan offline sobre CSV/JSON locales y carecen de ejecución dinámica o red.

**Consecuencias:**
- Unifica la marca visual entre `blandskron.cl` y KronPlan sin romper compatibilidad con instalaciones, enlaces ni sesiones existentes.
- Excluye `.agents/` de Ruff y Pytest en `pyproject.toml` para no contaminar la validación del proyecto Django.
- Establece en `ROADMAP.md` las cuatro fases verificables con gates de `pytest`, Playwright E2E, `axe-core` (WCAG 2.2 AA) y Lighthouse.
