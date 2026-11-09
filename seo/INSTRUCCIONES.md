# Sistema SEO autónomo de dulcesmarisol.es

Este documento es el **manual de trabajo** del agente de IA que se ejecuta cada
día como tarea programada. Cada ejecución empieza desde cero y solo sabe lo que
hay en esta carpeta, así que todo lo que deba recordarse tiene que quedar
escrito aquí.

## Objetivo

Que dulcesmarisol.es (WordPress + WooCommerce + Rank Math) consiga más tráfico
orgánico y más ventas desde Google, sobre todo en búsquedas de dulces
artesanos manchegos, dulces de Cuenca, rolletes, mantecados, pastas,
magdalenas, cajas de Navidad y regalos.

## Regla de oro: Marisol aprueba, el sistema ejecuta

**Nunca se cambia nada en la web sin aprobación.** El flujo es:

1. El agente audita y prepara propuestas concretas (texto actual → texto nuevo).
2. Las publica en una *issue* de GitHub del repositorio
   `losdulcesmarisol-stack/appmarisol` con la etiqueta `seo-propuesta`, una
   casilla `- [ ]` por propuesta, cada una con un identificador `[P-AAAAMMDD-N]`.
3. Marisol marca las casillas que aprueba (o comenta "aprobado todo",
   "no a P-…", o pide cambios en un comentario).
4. En la siguiente ejecución el agente aplica **solo** lo marcado/aprobado,
   lo registra en `cambios.json` y comenta en la issue qué se aplicó.
5. Si una issue no recibe respuesta en 14 días, se cierra como "sin respuesta"
   y sus propuestas pueden volver a proponerse más adelante.

Lo que el agente **sí puede hacer sin aprobación**: leer la web, auditar,
escribir en esta carpeta del repositorio, crear/comentar issues.

Lo que **nunca** hace aunque se apruebe por error: borrar productos, páginas o
entradas; cambiar precios, stock, pedidos, usuarios, ajustes de pago o
envío; instalar/desactivar plugins; cambiar URLs (slugs) sin crear antes la
redirección 301; tocar el tema o el código PHP.

## Rutina de cada ejecución

1. **Preparar**: `cd appmarisol` (o donde esté clonado), `git fetch origin
   claude/dulcesmarisol-online-store-69f4rf && git checkout
   claude/dulcesmarisol-online-store-69f4rf && git pull`.
2. **Leer memoria**: `seo/aprendizajes.md`, el último informe de
   `seo/historial/`, y `seo/cambios.json`.
3. **Aplicar lo aprobado**: buscar issues abiertas con etiqueta
   `seo-propuesta`; leer casillas marcadas y comentarios de Marisol
   (usuario `losdulcesmarisol-stack` o el dueño del repo). Aplicar con la API
   (ver abajo), comprobar en la web pública que el cambio se ve, anotar en
   `cambios.json` (fecha, id, URL, campo, antes, después) y comentar en la
   issue. Cerrar la issue cuando no quede nada pendiente.
4. **Auditar**: `python3 seo/scripts/auditoria.py`. Comparar con la auditoría
   anterior en `seo/datos/` (qué mejoró, qué empeoró, URLs nuevas o caídas).
5. **Medir resultados**: si hay acceso a datos de Search Console (ver abajo),
   comparar clics, impresiones y posición de las URLs cambiadas hace 14-28
   días frente a antes del cambio. Anotar conclusiones en `aprendizajes.md`.
6. **Proponer** como máximo **5 propuestas nuevas** por día, priorizadas por
   impacto esperado (errores > productos más vendidos/estacionales >
   resto). No repetir propuestas rechazadas (ver `aprendizajes.md`). Crear la
   issue del día con las propuestas, en español sencillo, explicando el
   porqué de cada una en una frase.
7. **Guardar**: escribir `seo/historial/AAAA-MM-DD.md` (resumen corto: qué se
   aplicó, qué cambió en la auditoría, qué se propone, enlaces a la issue),
   actualizar `aprendizajes.md` si hay algo nuevo que recordar, y hacer commit
   y push a la rama `claude/dulcesmarisol-online-store-69f4rf`.
8. **Avisar**: terminar con un resumen de 3-5 líneas (se envía como
   notificación al móvil).

Si algo falla (web caída, 401 en la API, etc.) se anota en el historial, se
avisa en el resumen final, y no se intenta "arreglar" el entorno.

## Cómo aplicar cambios (API de WordPress)

La contraseña de aplicación la inyecta el proxy del entorno en las peticiones
a `dulcesmarisol.es`; no hay que poner ninguna clave.

- Productos: `GET/PUT https://dulcesmarisol.es/wp-json/wc/v3/products/{id}`
  - `name`, `description`, `short_description`, `images[].alt`
  - Rank Math: `meta_data: [{"key":"rank_math_title","value":"..."},
    {"key":"rank_math_description","value":"..."},
    {"key":"rank_math_focus_keyword","value":"..."}]`
- Categorías de producto: `/wp-json/wc/v3/products/categories/{id}`
  (`description`).
- Páginas y entradas: `/wp-json/wp/v2/pages/{id}`, `/wp-json/wp/v2/posts/{id}`.
  Si los campos `meta.rank_math_*` no se pueden escribir por REST, usar el
  endpoint de Rank Math `POST /wp-json/rankmath/v1/updateMeta` con
  `{"objectType":"post","objectID":ID,"meta":{"rank_math_title":"..."}}`.
- Texto alternativo de imágenes: `POST /wp-json/wp/v2/media/{id}`
  con `alt_text`.

Antes de cada `PUT`, guardar el valor anterior en `cambios.json` para poder
deshacerlo. Después, cargar la URL pública y comprobar el cambio.

## Datos de Search Console

Rank Math puede tener el módulo *Analytics* conectado a Search Console. Si
está activo, sus datos se leen por la API de Rank Math con la misma
credencial (rutas `rankmath/v1/an/...`; si la ruta no existe, el módulo no
está conectado: anotarlo y seguir sin esos datos).

## Criterios SEO de la casa

- Títulos ≤ 60 caracteres, con la palabra clave al principio y "Dulces
  Marisol" al final si cabe. Metadescripciones de 120-155 caracteres, con
  una llamada a la acción (envío a toda España, hecho a mano en Cuenca).
- Cada producto con descripción **única** (≥ 150 palabras): ingredientes,
  cómo se elabora, para qué ocasión, conservación, peso/unidades. Nunca
  inventar ingredientes, alérgenos, premios ni datos que no estén ya en la
  web: si falta un dato, preguntarlo en la issue.
- Tono: cercano, artesano, familiar (obrador de cuarta generación en Cuenca).
- Estacionalidad: preparar contenido de Navidad desde octubre, Semana Santa
  desde febrero, Día de la Madre desde abril.
- Nada de relleno de palabras clave, texto oculto, reseñas falsas ni enlaces
  comprados.
