# Guía de Marca — KronPlan

> **Marca:** KronPlan
> **Descriptor:** Agile Planning & Estimation
> **Eslogan:** *Plan together. Build better.*
> **Firma:** Open Source · By BLANDSKRON

---

## 1. Posicionamiento y Relación con BLANDSKRON

**KronPlan** es la plataforma open source de planificación y estimación ágil de **BLANDSKRON**. Comparte el ADN visual de la casa matriz —fondo obsidiana profundo, acentos violeta/índigo de alta legibilidad, detalles cian de velocidad y tipografía técnica monoespaciada— adaptado a un espacio colaborativo humano, rápido y sin fricción.

### Personalidad de marca
- **Profesional y precisa:** diseñada para equipos de ingeniería, producto y diseño que estiman a diario sin ruido visual.
- **Colaborativa y justa:** protege la independencia de criterio (voto privado hasta el reveal) y evita cualquier mecanismo de presión social.
- **Lúdica con medida:** las mascotas, avatares y capa cosmética hacen la espera amena, siempre opcionales y subordinados a la reunión.

---

## 2. Arquitectura Verbal

| Elemento | Texto oficial | Uso |
| --- | --- | --- |
| **Nombre** | `KronPlan` | Siempre en PascalCase, una sola palabra. Nunca `Kron Plan` ni `kron-plan` en títulos visibles. |
| **Descriptor** | `Agile Planning & Estimation` | Subtítulo bajo el wordmark, metadatos y cabeceras de presentación. |
| **Eslogan** | `Plan together. Build better.` | Landing page, pantalla de ingreso/registro y tarjeta social. |
| **Firma** | `Open Source · By BLANDSKRON` | Pie de página, `README.md`, documentación y badges. |

---

## 3. El Isotipo y Sus Activos

El isotipo de KronPlan combina dos **cartas de planificación superpuestas** con una **letra `K` geométrica** integrada en la carta frontal y un **destello romboidal Velocity Cyan (`#22D3EE`)** en la esquina superior derecha. Simboliza la convergencia de criterios individuales en una estimación compartida.

### Catálogo de archivos en `static/brand/`

| Archivo | Uso recomendado | Fondo |
| --- | --- | --- |
| [`static/brand/kronplan-mark.svg`](../static/brand/kronplan-mark.svg) | Isotipo cromático principal (`64×64` base) | Oscuro o claro |
| [`static/brand/kronplan-logo-dark.svg`](../static/brand/kronplan-logo-dark.svg) | Lockup horizontal con descriptor para superficies oscuras | `#0D1020`, `#17182D` |
| [`static/brand/kronplan-logo-light.svg`](../static/brand/kronplan-logo-light.svg) | Lockup horizontal con descriptor para superficies claras | `#F5F7FB`, `#FFFFFF` |
| [`static/brand/kronplan-mono-light.svg`](../static/brand/kronplan-mono-light.svg) | Variante monocromática clara (`#F5F7FB`) | Oscuro / foto / acento |
| [`static/brand/kronplan-mono-dark.svg`](../static/brand/kronplan-mono-dark.svg) | Variante monocromática oscura (`#0D1020`) | Claro / impresión |
| [`static/brand/favicon.svg`](../static/brand/favicon.svg) | Ícono de navegador y PWA (`32×32` optimizado) | Cualquiera |
| [`static/brand/social-card.svg`](../static/brand/social-card.svg) | Tarjeta Open Graph (`1200×630`) y cabecera de `README.md` | `#0D1020` |

### Zona de respeto y tamaños mínimos
- **Zona de respeto:** mínimo `0.25 ×` el ancho del isotipo alrededor de los cuatro lados.
- **Tamaño mínimo digital:** `24×24 px` para el isotipo; `16×16 px` exclusivamente usando `favicon.svg`; `140 px` de ancho mínimo para el lockup completo con descriptor.

### Usos incorrectos (Prohibido)
1. No deformar proporciones ni cambiar el ángulo de rotación entre las dos cartas.
2. No reemplazar la `K` ni reintroducir siglas anteriores (`PP`).
3. No aplicar sombras pesadas o brillos neón fuera de los definidos en el sistema de diseño.
4. No usar el logo oscuro sobre fondos oscuros ni el claro sobre papel blanco.

---

## 4. Tono de Voz

- **Claro y directo:** mensajes cortos orientados a la acción (*"Elige una carta"*, *"Revelar votos"*, *"Tu elección permanece privada hasta el reveal"*).
- **Transparente:** explicar con honestidad qué hace el sistema (especialmente en errores 404/500, expulsión de sala o sala llena).
- **Respetuoso:** sin urgencia artificial ni contadores punitivos sobre quién tarda más en votar.
