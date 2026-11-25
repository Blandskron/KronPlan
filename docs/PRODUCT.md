# KronPlan — Producto y UX

## 1. Visión del Producto
Alternativa gratuita, moderna, profesional, rápida y sencilla de usar a Planning Poker Online.
Flujo central: Crear sala → compartir enlace → escribir nombre → votar.

## 2. Personas

### Persona 1: Facilitador
- **Perfil**: Scrum Master, Product Owner o Tech Lead.
- **Necesidades**: Crear salas rápidamente sin fricción. Compartir el link al instante por chat o videollamada. Controlar el flujo de la sesión (cuándo se revela, cuándo se reinicia). Mantener el enfoque del equipo en la estimación.
- **Permisos**: Crear sala, invitar, iniciar votación, revelar, reiniciar, cerrar sala, gestionar tareas (issues), alternar entre la baraja corta y la completa, y **expulsar a un participante** de la sala (ver ADR-007).

### Persona 2: Participante Invitado
- **Perfil**: Desarrollador, QA o Diseñador de un equipo ágil.
- **Necesidades**: Entrar a la sala con un solo click y su nombre, sin crear cuenta. Entender inmediatamente cómo votar. Ver quién más está en la sala. Conocer los resultados una vez revelados.
- **Permisos**: Entrar, votar, cambiar voto (antes del reveal), salir. NO puede revelar, gestionar la sala, cambiar la baraja ni expulsar a nadie. Puede ser expulsado por el facilitador.

## 3. Flujos Principales

### Flujo: Crear Sala (Facilitador)
1. Usuario abre la Landing Page.
2. Inicia sesión (o crea cuenta si no tiene).
3. Accede al Dashboard (lista de salas pasadas/activas).
4. Hace click en "Nueva Planning Poker".
5. Entra a la nueva sala (ej: `/p/7Xs92Klm`).
6. Copia el enlace y lo comparte con su equipo.

### Flujo: Entrar como Invitado (Participante)
1. Abre el enlace compartido.
2. Ve una pantalla de "Ingreso de nombre" (ej. placeholder: "Tu nombre...").
3. Escribe su nombre y presiona "Entrar".
4. Accede a la sala como participante activo.

### Flujo: Votación
1. El facilitador lee/añade la historia a estimar.
2. Cada participante selecciona una carta de la baraja (ej. 1, 2, 3, 5, 8...).
3. Mientras se vota, todos ven quiénes han votado (estado: ✅), pero NO el valor.
4. Cuando el equipo termina de votar, el facilitador presiona "Reveal".
5. Todos ven instantáneamente los votos, el promedio (si aplica), y si hay consenso.
6. Discuten si es necesario.
7. Facilitador presiona "Siguiente ronda" o "Reiniciar" para continuar.

## 4. Arquitectura de Información e Interfaz (Sala)

### Layout Principal
- **Header**: Nombre de la sala, enlace rápido para copiar, estado de conexión.
- **Sidebar (o panel superior/izquierdo)**: Lista de Issues/Tareas.
- **Centro (Mesa)**: Área principal con la historia actual, estado ("Votando...", "Resultados"), y avatares/nombres de participantes con sus estados de voto (pensando / votó / [Valor]).
- **Bottom (Baraja)**: Cartas grandes y accesibles. Por defecto ocho —`0, 1, 2, 3, 5, 8, 13, ?`—; el facilitador las amplía a `0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ?, ☕` con el interruptor «Baraja larga». Trece cartas en un teléfono se recorren de lado.
- **Controles de Facilitador**: Botones flotantes o en bloque central: "Reveal", "Reiniciar", "Siguiente".

## 5. Design System

La especificación completa de identidad visual y tokens vive en [`docs/BRAND_GUIDELINES.md`](BRAND_GUIDELINES.md) y [`docs/DESIGN_SYSTEM.md`](DESIGN_SYSTEM.md).

El frontend declara una sola vez sus primitivas de marca `--kp-*` en `static/css/style.css` y las traduce a los tokens semánticos que consumen los componentes (`--bg`, `--surface`, `--accent`, `--felt`…).

- **Temas:** modo oscuro por defecto (`dark`), modo claro (`light`) y preferencia del sistema (`system`), almacenados en navegador y verificados bajo WCAG 2.2 AA.
- **Tipografía:** **Sora** (títulos/display), **Inter** (interfaz/cuerpo) y **JetBrains Mono** (cartas, códigos y cifras tabulares), con respaldo del sistema.
- **Escala, forma y movimiento:** base espacial de 4 px, radios de `8/12/16/24/999 px`, iconografía Lucide SVG (`templates/partials/_icons.html`), microinteracciones de 150–250 ms y respeto estricto de `prefers-reduced-motion`.

### La regla que más fácil se rompe

**Una superficie que no cambia con el tema no puede llevar texto de un token que sí cambia.**

Hay tres de esas superficies: la **cara de la carta** (`--card-face`, clara siempre, porque una carta es un objeto claro), el **panel de marca** del login y el registro (oscuro siempre) y el **paño** (`--felt`). El texto encima debe derivarse de la propia superficie (`--card-ink` o tokens fijos calibrados para esa superficie) y nunca usar tokens variables entre temas como `--muted` o `--text-soft`.

### Carcasa móvil

Por debajo de 821px la interfaz deja de comportarse como una página y pasa a comportarse como una
aplicación. Ver `docs/ROOM_VISUAL_DESIGN.md` para el detalle de la sala; en resumen:

- Barra superior fija y compacta con la identidad y el tema, respetando `env(safe-area-inset-top)`.
- **Barra de pestañas inferior** con los destinos de la app. Antes los enlaces del encabezado
  simplemente desaparecían en pantalla pequeña y no reaparecían en ningún sitio: el usuario de
  teléfono se quedaba sin crear sala ni cerrar sesión.
- En la sala, la baraja se ancla encima de la barra de pestañas inferior, reservando la suma de ambas alturas para votar con un solo toque sin perder la navegación.
- `100dvh` en lugar de `100vh`, y `env(safe-area-inset-*)` en todo lo anclado.
