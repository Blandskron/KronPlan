# Roadmap de Evolución — KronPlan (Agile Planning & Estimation)

> **Marca oficial:** KronPlan — Agile Planning & Estimation
> **Eslogan:** *Plan together. Build better.*
> **Ecosistema:** Open Source · By BLANDSKRON
> **Estado actual:** Fase 1 completada · Próxima etapa: Fase 2 (Branding y Design System)

---

## 1. Resumen Ejecutivo y Auditoría Integral (Fase 1)

### 1.1 Estado actual del repositorio
- **Arquitectura:** Monolito modular en **Python 3.12+ / Django 6.1** (`accounts`, `rooms`, `config`), **Django Channels + Daphne + Redis**, **HTML/CSS/Vanilla JS nativo** sin frameworks SPA ni build steps pesados.
- **Autoridad y privacidad:** Validada en servidor (`rooms/services.py`, `rooms/consumers.py`), con CSP estricto por *nonce* en `config/middleware.py`, throttling por usuario en `accounts/throttling.py` y privacidad garantizada de los votos hasta el `reveal`.
- **Calidad y pruebas base (medidas en Fase 1):**
  - `ruff check .`: **0 errores**.
  - `pytest . --cov`: **151 tests pasando**, **85,62 %** de cobertura total (umbral CI: 80 %; `rooms/services.py` al 96 %, `rooms/consumers.py` al 78 %).
  - `pytest -m e2e`: **33 tests Playwright** cubriendo geometría del anillo elíptico (1–14+ participantes), abanico de cartas, identidades SVG, coreografía de revelación, capa cosmética de juego, modo recreo y carcasa móvil.
  - `manage.py check` y `makemigrations --check --dry-run`: **0 problemas**.
- **Superficie visual actual:** 13 plantillas Django (`templates/`) y 1 hoja `static/css/style.css` basadas en la paleta magenta/azul heredada (`#ed117b` / `#202b70`, tipografía Manrope + Inter, clave de tema `planning-pocket-theme`).
- **Deuda técnica heredada en `PLAN.md`:**
  1. Cobertura de caminos de borde en `rooms/consumers.py` (errores de despacho, múltiples pestañas con `connection_count`, `player.moved` bajo 110 ms o recreo cerrado).
  2. Test de integración contra un Redis real que valide supervivencia del WebSocket > 6 s (el `socket_timeout=20` ya está implementado en `config/settings.py` y verificado estructuralmente en `rooms/test_channel_layer.py`).
  3. Barra inferior apilada con la mano de cartas en móvil dentro de la sala (`body.is-room .app-tabbar`).

### 1.2 Auditoría del ecosistema corporativo BLANDSKRON
Tras analizar `https://blandskron.cl/` y el repositorio `https://github.com/Blandskron/blandskronSPA`:
- **Tokens reales de BLANDSKRON:** `--violet: #4a148c`, `--deep: #2e0b59`, `--accent: #8b5cf6`, `--lavender: #c4b5fd`, `--black: #090909`, `--ink: #15121b`, `--paper: #f8f7fa`, `--line: #e6e2ec`, radios `21px` / `11px`, tipografía `Inter Variable` + `Manrope Variable` + `JetBrains Mono Variable`.
- **Prácticas de ingeniería y accesibilidad de BLANDSKRON:** `focus-visible` de doble anillo de alto contraste, *skip-link*, validación W3C, auditoría automatizada con `axe-core` y mediciones reproducibles de Lighthouse.
- **Conclusión estratégica:** Reemplazar la paleta magenta/azul heredada por la identidad **KronPlan** (violeta `#7C3AED` / `#A78BFA`, índigo `#6366F1`, cian `#22D3EE`, obsidiana `#0D1020`) alinea el producto directamente con el ADN visual violeta/obsidiana/monoespaciado de **BLANDSKRON**, conservando la arquitectura ligera y la geometría verificada de la mesa.

### 1.3 Incorporación auditada de la skill `ui-ux-pro-max`
- **Ubicación:** `.agents/skills/ui-ux-pro-max/` (fijada al commit `8db36338810d` de `nextlevelbuilder/ui-ux-pro-max-skill`, licencia MIT).
- **Auditoría de seguridad:** 6 scripts Python auditados línea por línea; usan únicamente biblioteca estándar de Python, operan 100 % offline sobre catálogos CSV/JSON locales y no contienen llamadas de red, telemetría, `subprocess`, `eval`, `exec` ni carga dinámica. Excluidos de `ruff` y `pytest` en `pyproject.toml`.
- **Resultados aplicados al proyecto:**
  - *Estilo y producto:* `Soft UI Evolution` + `Minimalism & Swiss Style` + `Micro-interactions` sobre `Dark Mode` de alto contraste, evitando emojis como iconos (solo SVG Lucide/propios), exigiendo `cursor: pointer`, transiciones de 150–250 ms y respeto estricto a `prefers-reduced-motion`.
  - *Tipografía:* combinación de display geométrica (**Sora**) + cuerpo altamente legible (**Inter**) + valores técnicos/cartas/códigos (**JetBrains Mono**, con `tabular-nums` en métricas y resultados).
  - *UX / Accesibilidad:* controles compactos como `<button aria-pressed>` reales (nunca `<div>` clicables), navegación completa por teclado sin trampas de foco, y gráficos de distribución que no dependan solo del color.

### 1.4 Patrones UX/UI de herramientas ágiles y Planning Poker (Linear, Jira, Scrum)
1. **Contexto primero (Master-Detail):** La historia activa (título, descripción, identificador/estado y cola) permanece visible junto a la mesa para evitar cambios de pestaña.
2. **Mesa de tres estados sin sesgo de anclaje:**
   - *Pensando:* avatar/mascota + carta en espera sutil, sin presión visual.
   - *Votó:* reverso geométrico KronPlan + indicador claro sin exponer valor.
   - *Revelado:* giro simultáneo/escalonado controlado por servidor, agrupación visual y resaltado de consenso vs. dispersión (*outliers*) para guiar la conversación del equipo.
3. **Velocidad operativa para equipos técnicos:** Atajos de teclado opcionales en la baraja (`0–9`, `?`, `Escape` para limpiar/cerrar popovers) sin interferir con campos de texto ni lectores de pantalla.
4. **Gamificación ética y opcional (ADR-005):** Objetos blandos y recreo siempre subordinados a la estimación, con doble interruptor (sala + usuario) y `prefers-reduced-motion` mandatorio.

### 1.5 Revalidación matemática WCAG 2.2 AA de la paleta KronPlan
Cálculo verificado de luminancia relativa y ratio de contraste (mínimo **4,5:1** texto normal, **3,0:1** texto grande / componentes UI):

| Token / Color | Hex | Sobre Dark (`#0D1020` / `#17182D` / `#211F38`) | Sobre Light (`#F5F7FB` / `#FFFFFF`) | Decisión técnica revalidada (WCAG 2.2 AA) |
| --- | --- | --- | --- | --- |
| Text Primary Dark | `#F5F7FB` | `17,61` / `16,25` / `14,86` | N/A | Texto principal en Dark Mode. |
| Text Muted Dark | `#B8B3CD` | `9,32` / `8,60` / `7,87` | N/A | Texto secundario/subtítulos en Dark Mode. |
| Agile Violet | `#A78BFA` | `6,94` / `6,40` / `5,86` | `2,54` / `2,72` | `--accent` de texto, enlaces y *eyebrows* en Dark Mode. Decorativo en Light. |
| Planning Purple | `#7C3AED` | `3,31` / `3,06` / `2,80` | `5,31` / `5,70` | **Ajuste 1:** Fondo de botón primario (`#FFFFFF` encima = `5,70:1`, pasa AA) y bordes/brillos. No usar como texto sobre fondo oscuro. |
| Light Accent (AA) | `#6D28D9` | `2,66` | `6,62` / `7,10` | **Ajuste 4:** Texto interactivo, enlaces y *hover* primario en Light Mode. |
| Collaboration Indigo | `#6366F1` | `4,23` / `3,90` / `3,57` | `4,16` / `4,47` | Gradientes, bordes de foco, íconos ≥ 3:1 y superficies secundarias. En Light texto usar `#4F46E5` (`5,86:1`). |
| Velocity Cyan | `#22D3EE` | `10,45` / `9,64` / `8,82` | `1,68` / `1,81` | Highlights/datos sobre Dark y paño. En Light texto usar `#0E7490` (`5,00:1`). |
| Soft Lavender | `#DDD6FE` | `13,60` / `12,55` / `11,48` | `1,29` | Anillos de foco (`--ring`), superficies tintadas suaves y texto destacado en Dark. |
| Completed | `#22C55E` | `8,29` / `7,65` / `6,99` | `2,12` / `2,28` | Dark texto/icono. Light texto: `#15803D` (`4,68` / `5,02`). |
| Pending | `#F59E0B` | `8,79` / `8,11` / `7,42` | `2,00` / `2,15` | Dark texto/icono. Light texto: `#B45309` (`4,68` / `5,02`). |
| Error | `#EF4444` | `5,02` / `4,63` / `4,23` | `3,51` / `3,76` | **Ajuste 2:** Sobre tarjetas elevadas (`#211F38`) da `4,23:1` (< 4,5). Usar `#F87171` para texto de error en Dark y `#DC2626` (`4,50` / `4,83`) en Light; `#EF4444` en bordes/iconos. |
| Information | `#38BDF8` | `8,81` / `8,14` / `7,44` | `2,00` / `2,14` | Dark texto/icono. Light texto: `#0369A1` (`5,53` / `5,93`). |
| Consensus | `#14B8A6` | `7,59` / `7,00` / `6,40` | `2,32` / `2,49` | Dark texto/pulso de unanimidad. Light texto: `#0F766E` (`5,10` / `5,47`). |
| Inactive | `#64748B` | `3,97` / `3,66` / `3,35` | `4,44` / `4,76` | **Ajuste 3:** Usar `#94A3B8` (`6,22–7,36:1`) en Dark y `#475569` (`>6,5:1`) en Light para texto inactivo; conservar `#64748B` en bordes/puntos. |

> **Invariante crítica conservada (ADR-006 / ADR-009):** Ninguna de las tres superficies fijas (cara de la carta, panel de marca oscuro en auth, y paño de la mesa) debe usar tokens de texto que inviertan con el tema.

---

## 2. Roadmap por Fases

### Fase 1 — Investigación y planificación *(Completada)*
- [x] Auditoría completa del repositorio, tests, middleware CSP, consumidores WebSocket, estilos y plantillas.
- [x] Auditoría de `blandskron.cl` y `Blandskron/blandskronSPA`.
- [x] Auditoría de seguridad y compatibilidad e instalación local de `.agents/skills/ui-ux-pro-max` (commit `8db36338810d`).
- [x] Investigación UX/UI de patrones de Planning Poker, Linear, Jira y Scrum.
- [x] Revalidación matemática WCAG 2.2 AA de paleta y tipografía.
- [x] Registro de `ADR-009` en `docs/DECISIONS.md` y creación de `ROADMAP.md`.

---

### Fase 2 — Branding y Design System
**Objetivo:** Definir y materializar la identidad visual de **KronPlan** y su sistema de tokens y componentes reutilizables antes de migrar las vistas.

- **Etapa 2.1 — Documentación de Marca y Sistema de Diseño**
  - Crear `docs/BRAND_GUIDELINES.md`: identidad ("KronPlan — Agile Planning & Estimation", "Plan together. Build better.", "Open Source · By BLANDSKRON"), construcción del isotipo (K geométrica + cartas superpuestas), grilla de seguridad, variantes de color/monocromo, usos indebidos, tono de voz y relación con el ecosistema BLANDSKRON.
  - Crear `docs/DESIGN_SYSTEM.md`: arquitectura de tokens `--kp-*` y semánticos, modos Dark (defecto) / Light / Sistema, escala tipográfica (`Sora`, `Inter`, `JetBrains Mono`), escala espacial base `4 px`, radios `8 / 12 / 16 / 24 px` + `999px` en píldoras interactivas, elevación, *glassmorphism* sutil y matriz de contraste WCAG 2.2 AA.
- **Etapa 2.2 — Activos Vectoriales Originales (`static/brand/`)**
  - Diseñar `static/brand/kronplan-mark.svg` (isotipo K geométrica integrada con cartas en capas).
  - Diseñar `static/brand/kronplan-logo-dark.svg` y `kronplan-logo-light.svg` (isotipo + wordmark + descriptor).
  - Diseñar `static/brand/kronplan-mono-light.svg` y `kronplan-mono-dark.svg` (variantes monocromáticas).
  - Diseñar `static/brand/favicon.svg` (optimizado a 16×16 y 32×32) y `static/brand/social-card.svg` (1200×630 Open Graph).
- **Etapa 2.3 — Capa de Design Tokens CSS e Iconografía Lucide SVG**
  - Refactorizar el bloque raíz de `static/css/style.css` hacia primitivas `--kp-*` y temas `[data-theme="dark"]` (canónico por defecto) y `[data-theme="light"]`, aplicando todos los ajustes AA de la Sección 1.5.
  - Cargar tipografías `Sora`, `Inter` y `JetBrains Mono` (actualizando `base.html` y CSP si aplica) con respaldos de sistema.
  - Construir un sprite o parcial de iconografía **Lucide SVG** reutilizable (`templates/partials/_icons.html`) eliminando caracteres tipográficos improvisados en botones/estados y refinando `templates/rooms/_table_sprite.html` (mascotas, caras, objetos lanzables e ítems de recreo con línea geométrica unificada KronPlan).

**Criterios de aceptación verificables (Fase 2):**
1. Todos los SVG en `static/brand/` son válidos XML, auto-contenidos (sin scripts ni recursos externos) y compatibles con `CSP img-src 'self' data:`.
2. Script automatizado de verificación de contraste confirma **0 pares texto/fondo < 4,5:1** en tokens Dark y Light.
3. `collectstatic --noinput` procesa los nuevos activos sin errores y la suite de 151 tests + `ruff` sigue en verde.

---

### Fase 3 — Implementación Integral del Frontend y Transición de Marca
**Objetivo:** Llevar la nueva identidad y UX de clase internacional a cada pantalla y flujo del producto sin romper contratos de servidor ni frameworks nativos.

- **Etapa 3.1 — Tema de 3 estados (Dark por defecto / Light / Sistema) y Chrome Global**
  - Implementar selector cíclico o menú accesible de tema (`dark`, `light`, `system`) en `templates/base.html`, aplicando **Dark Mode por defecto** cuando no exista preferencia guardada o el sistema no fuerce claro, y migrando transparentemente `localStorage['planning-pocket-theme']` → `kronplan-theme` (y equivalentes de sonido/efectos).
  - Actualizar `templates/base.html`, `templates/404.html` y `templates/500.html` con marca **KronPlan**, isotipo SVG, firma *Open Source · By BLANDSKRON*, `<link rel="icon">` y metadatos Open Graph.
- **Etapa 3.2 — Landing Page, Auth, Dashboard Bento Grid y Flujos de Entrada**
  - Convertir `/` para usuarios **no autenticados** en una **Landing Page de KronPlan** (Hero + demo visual de mesa interactiva + Bento Grid de capacidades + flujo en 3 pasos + CTA a crear cuenta/ingresar), manteniendo la redirección automática a `dashboard` para usuarios ya autenticados y compatibilidad total de rutas existentes.
  - Rediseñar `templates/accounts/dashboard.html` con **Bento Grid** (métricas rápidas de salas activas/cerradas, acceso directo a nueva sala, tarjetas de sesión enriquecidas y estado vacío refinado).
  - Rediseñar `templates/registration/login.html`, `templates/registration/register.html`, `templates/rooms/create_room.html`, `templates/rooms/join_guest.html` y las pantallas de estado (`close_room_confirm.html`, `room_closed.html`, `room_full.html`, `room_removed.html`) con estética Modern Agile Workspace / Glassmorphism sutil. **Corregir defecto visual detectado en auditoría (`1440×900`):** en `login.html` actual `.auth-deck` (`position: absolute; bottom: 3rem`) se solapa sobre el párrafo de `.auth-promise`; pasarlo a flujo flex/grid o espaciado reservado con verificación en captura real.
- **Etapa 3.3 — Mesa Colaborativa, Cartas Exclusivas y UX de Sesión**
  - Rediseñar las cartas de Planning Poker (abanico inferior y cartas en mesa): reverso geométrico KronPlan con patrón de precisión + isotipo `K`, cara de carta limpia con `JetBrains Mono` y `tabular-nums`, diferenciación visual clara para cartas especiales (`?`, `Coffee`).
  - Perfeccionar estados de votación y coreografía de revelación: giro 3D suave (`150–250 ms` microinteracciones), pulso de consenso en `#14B8A6` (teal), panel de resultados con estadísticas claras y barras interactivas con resaltado de consenso/extremos, respetando `prefers-reduced-motion`.
  - Añadir atajos de teclado en la mesa (`0–9`, `?` para votar cuando el foco no está en un input, flechas en la baraja y mesa) y barra de estado de conexión / copiar enlace con confirmación accesible (`aria-live`).
  - Resolver deuda móvil de `PLAN.md`: apilar `.app-tabbar` y la mano de cartas en `body.is-room` (`bottom: var(--tabbar-height)`, ajuste de `--deck-dock-height` y actualización de `test_the_hand_is_docked_to_the_bottom_edge_of_a_phone`).
- **Etapa 3.4 — Transición Completa de Marca, Documentación y Metadatos**
  - Actualizar `README.md` (insignias hacia `Blandskron/KronPlan`, captura/visuales actualizados, descripción oficial), `pyproject.toml`, `.github/` (workflows y plantillas) y documentación interna (`docs/PRODUCT.md`, `docs/ARCHITECTURE.md`, `docs/DEVELOPER_GUIDE.md`, `docs/SECURITY.md`, `docs/ROOM_VISUAL_DESIGN.md`), conservando compatibilidad de nombres internos de BD/migraciones y env vars existentes.

**Criterios de aceptación verificables (Fase 3):**
1. Todas las rutas existentes (`/`, `/accounts/login/`, `/accounts/register/`, `/accounts/dashboard/`, `/create/`, `/p/<public_id>/`, `/p/<public_id>/close/`, `/health/`) funcionan preservando contratos HTTP/WebSocket y privacidad pre-reveal.
2. En móvil (`390×844`), 0 desbordamiento horizontal (`scrollWidth <= innerWidth`), barra de pestañas + baraja apiladas sin taparse ni tapar el contenido, objetivos táctiles ≥ 44×44 px.
3. No se introducen dependencias JS/SPA externas; CSP con nonce estricto sigue activo sin violaciones de consola.

---

### Fase 4 — Validación, Auditoría y Perfeccionamiento
**Objetivo:** Cerrar la deuda de cobertura/Redis, ejecutar pruebas multi-participante y certificar calidad visual, funcional y de accesibilidad.

- **Etapa 4.1 — Cobertura y Robustez en Tiempo Real**
  - Cubrir en `rooms/test_websockets.py` los 3 caminos pendientes de `PLAN.md` (`rooms/consumers.py`: errores de despacho, ciclo multi-pestaña con `connection_count`, `player.moved` throttle/recreo cerrado) elevando la cobertura general por encima del 87 %.
  - Añadir test opcional/marcado o verificación reproducible contra Redis real (> 6 s de espera en socket) documentado en `docs/TESTING.md`.
- **Etapa 4.2 — Suite E2E Multi-Participante y Tiempo Real (Playwright + ASGI)**
  - Ampliar tests E2E para verificar con navegador real (y sesiones concurrentes / ASGI cuando corresponda): múltiples participantes, reconexión WebSocket tras corte, **no transmisión de votos en payloads WS antes de `reveal_round`**, permisos estrictos de facilitador vs. invitado, expulsión con veto, cambio de baraja y revelación sincronizada.
- **Etapa 4.3 — Accesibilidad (WCAG 2.2 AA / axe-core), Lighthouse y Regresión Visual**
  - Ejecutar `axe-core` vía Playwright en todas las pantallas principales (Landing, Login, Register, Dashboard, Create Room, Join Guest, Room Detail en estados `voting`, `revealed` y `recess`) tanto en **Dark Mode** como en **Light Mode**, exigiendo **0 violaciones**.
  - Ejecutar **Lighthouse** (Performance, Accessibility, Best Practices, SEO) y verificar métricas objetivo (Accessibility ≥ 95, Best Practices ≥ 95, SEO ≥ 90).
  - Capturar screenshots reales en escritorio (`1440×900`) y móvil (`390×844`) en ambos temas para inspección visual y actualizar la documentación del proyecto.
- **Etapa 4.4 — Cierre de Quality Gates y Limpieza Final**
  - Ejecutar exactamente el pipeline de CI: `ruff check .`, `pytest . --cov`, `manage.py check --deploy` (`DEBUG=False`), `collectstatic`, `makemigrations --check --dry-run` y `DJANGO_ALLOW_ASYNC_UNSAFE=true pytest -m e2e`.
  - Limpiar tareas completadas de `PLAN.md` siguiendo `AGENTS.md`.

**Criterios de aceptación verificables (Fase 4):**
1. Cobertura de `rooms/services.py` ≥ 90 % y cobertura general ≥ 85 % (superando el umbral de CI del 80 %).
2. 0 violaciones `axe-core` WCAG 2.2 AA en dark y light mode.
3. Todos los tests unitarios, de integración, E2E y checks de despliegue pasan tras la última edición sin skips ni aserciones relajadas.
