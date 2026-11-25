# Design System — KronPlan

> Sistema visual oficial de **KronPlan — Agile Planning & Estimation** (`Open Source · By BLANDSKRON`).
> Implementado nativamente con variables CSS (`--kp-*` → tokens semánticos) en [`static/css/style.css`](../static/css/style.css), sin frameworks SPA ni pasos de compilación externos.

---

## 1. Arquitectura en Dos Capas

1. **Capa de Primitivas (`--kp-*`):** declara una sola vez la paleta de marca, neutros, semánticos, escala espacial (4 px), radios y tiempos de transición. Ningún componente consume `--kp-*` directamente.
2. **Capa Semántica:** traduce las primitivas a roles consumidos por la interfaz (`--bg`, `--surface`, `--text`, `--primary`, `--accent`, `--felt`, `--consensus`…). Cambiar entre Dark Mode (canónico) y Light Mode sólo reasigna esta traducción.

---

## 2. Paleta de Color y Revalidación WCAG 2.2 AA

### Colores de marca y neutros

| Primitiva | Valor | Rol |
| --- | --- | --- |
| `--kp-violet-400` | `#A78BFA` | **Agile Violet:** acento legible sobre superficies oscuras (`5,86–6,94:1`), bordes activos y subtítulos de marca. |
| `--kp-purple-600` | `#7C3AED` | **Planning Purple:** fondo de botones primarios (con texto `#FFFFFF` = `5,70:1`) y acento decorativo. |
| `--kp-purple-700` | `#6D28D9` | **Deep Purple (AA Light):** acento de texto/enlaces sobre claro (`6,62–7,10:1`) y estado hover de botón primario (`7,10:1`). |
| `--kp-indigo-500` | `#6366F1` | **Collaboration Indigo:** gradientes, reversos de carta y bordes interactivos (texto en claro `#4F46E5`, `5,86:1`). |
| `--kp-cyan-400` | `#22D3EE` | **Velocity Cyan:** acento técnico de alto impacto en Dark Mode (`8,82–10,45:1`; en claro `#0E7490`, `5,00:1`). |
| `--kp-lavender-200` | `#DDD6FE` | **Soft Lavender:** anillos de foco (`--ring`), texto destacado sobre oscuro (`11,48–13,60:1`). |
| `--kp-neutral-950` | `#0D1020` | Fondo base canónico (Dark Mode). |
| `--kp-neutral-900` | `#17182D` | Superficie principal / chrome translúcido oscuro. |
| `--kp-neutral-850` | `#211F38` | Tarjetas elevadas y modales en Dark Mode. |
| `--kp-neutral-700` | `#34314D` | Bordes y divisores estructurales oscuros. |
| `--kp-neutral-50` | `#F5F7FB` | Texto principal en Dark Mode / Fondo base en Light Mode. |
| `--kp-neutral-300` | `#B8B3CD` | Texto secundario en Dark Mode (`7,87–9,32:1`). |

### Colores semánticos (calibrados AA por tema)

| Estado | Primitiva base | Token Dark (`--*`) | Token Light (`--*`) |
| --- | --- | --- | --- |
| **Completed** | `#22C55E` | `#22C55E` (`6,99:1`) | `#15803D` (`4,68:1`) |
| **Pending** | `#F59E0B` | `#F59E0B` (`7,42:1`) | `#B45309` (`4,68:1`) |
| **Error** | `#EF4444` | `#F87171` (`5,76:1` texto) / `#EF4444` borde | `#DC2626` (`4,50:1`) |
| **Information** | `#38BDF8` | `#38BDF8` (`7,44:1`) | `#0369A1` (`5,53:1`) |
| **Voting** | `#A78BFA` | `#A78BFA` (`5,86:1`) | `#6D28D9` (`6,62:1`) |
| **Consensus** | `#14B8A6` | `#14B8A6` (`6,40:1`) | `#0F766E` (`5,10:1`) |
| **Inactive** | `#64748B` | `#94A3B8` (`6,22:1` texto) | `#475569` (`7,07:1` texto) |

### Invariante de las Tres Superficies Fijas (ADR-006 / ADR-009)
Una superficie que **no cambia con el tema** jamás puede consumir un token de texto que **sí cambia**:
1. **Cara de la carta (`--card-face: #F8F7FC`):** siempre clara; su tinta (`--card-ink: #121024`) y su estado sin voto (`color-mix(in srgb, var(--card-ink) 64%, var(--card-face))` ≈ `6,59:1`) derivan de sí misma.
2. **Panel de marca oscuro (`.auth-promise`, `.form-card-visual`):** siempre oscuro (`#17182D` → `#0D1020`); usa `.eyebrow-light` (`#DDD6FE`, `12,55:1`) y texto `#F5F7FB` / `#B8B3CD`.
3. **Paño de la mesa (`--felt: #1E1B3A`, `--felt-deep: #111228`):** siempre oscuro en ambos temas para mantener legible la paleta de los 7 colores de asiento; usa `--felt-text: #C9C4E3` (`9,89:1`).

---

## 3. Tipografía

| Rol | Familia | Pesos | Uso |
| --- | --- | --- | --- |
| `--font-display` | `Sora` | `600`, `700`, `800` | Encabezados `h1`–`h3`, marca, valores grandes de resultados (`letter-spacing: -0.03em`). |
| `--font-sans` | `Inter` | `400`, `500`, `600`, `700` | Navegación, formularios, descripciones, badges y controles. |
| `--font-mono` | `JetBrains Mono` | `500`, `600`, `700` | Cartas de Fibonacci, códigos de sala (`#public_id`), cifras estadísticas (`tabular-nums`). |

---

## 4. Espaciado, Radios, Elevación y Movimiento

- **Escala espacial base de 4 px:** `--kp-space-1: 4px`, `--kp-space-2: 8px`, `--kp-space-3: 12px`, `--kp-space-4: 16px`, `--kp-space-5: 20px`, `--kp-space-6: 24px`, `--kp-space-8: 32px`, `--kp-space-10: 40px`, `--kp-space-12: 48px`, `--kp-space-16: 64px`.
- **Radios oficiales:**
  - `--radius-sm: 8px` (badges internos, botones compactos, cartas pequeñas)
  - `--radius-md: 12px` (inputs, cartas de baraja, ítems de lista)
  - `--radius-lg: 16px` (tarjetas de sala, paneles de resultado, mesa)
  - `--radius-xl: 24px` (contenedores principales, auth card, bottom-sheet móvil)
  - `--radius-pill: 999px` (botones de acción, switches, status pills)
- **Glassmorphism sutil:** `--chrome` + `backdrop-filter: blur(20px) saturate(1.35)` en barra superior, dock móvil y toast, combinado con borde luminoso superior `inset 0 1px 0 rgba(255, 255, 255, 0.08)` en tarjetas oscuras.
- **Microinteracciones (150–250 ms):**
  - `--ease: cubic-bezier(0.22, 0.61, 0.36, 1)`
  - `--dur-fast: 0.16s`, `--dur-mid: 0.22s`, `--dur-slow: 0.32s`
  - **Presupuesto GPU:** animaciones restringidas a `transform` y `opacity`; `@media (prefers-reduced-motion: reduce)` reduce duraciones a `0.01ms`.

---

## 5. Iconografía y Sprites Vectoriales

- **Iconografía UI (estilo Lucide SVG):** centralizada en [`templates/partials/_icons.html`](../templates/partials/_icons.html) (`viewBox="0 0 24 24"`, trazo `1.8`, esquinas redondeadas `round`, heredando `currentColor`).
- **Sprites de mesa:** [`templates/rooms/_table_sprite.html`](../templates/rooms/_table_sprite.html) unifica mascotas, caras, objetos lanzables y puntos de recreo usando tinta obsidiana `#0D1020` y acentos de KronPlan.
- **Clases reutilizables del sistema:** `.kp-icon`, `.kp-badge`, `.kp-glass`, `.kp-bento` declaradas en [`static/css/style.css`](../static/css/style.css).
