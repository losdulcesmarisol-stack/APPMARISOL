# Propuestas SEO para dulcesmarisol.es

**Cómo responder:** pulsa el lápiz ✏️ de arriba a la derecha. Cambia `- [ ]` por
`- [x]` para **aprobar** o por `- [-]` para **rechazar**. Para comentar, escribe
debajo una línea que empiece por `> Marisol:`. Después pulsa **"Commit changes"**.

## Pendientes

- [ ] **[P-20261109-1]** Metadescripción de la categoría "Dulces Marisol" del blog
  (https://dulcesmarisol.es/category/dulces-marisol/). Ahora no tiene ninguna, y
  Google se inventa una.
  - Nueva: «Noticias, recetas y novedades de Dulces Marisol, obrador familiar de
    dulces manchegos artesanos en Cuenca. Descubre nuestros rolletes, mantecados y más.»
  - *(Se aplicará cuando funcione el acceso a la API de WordPress.)*

- [ ] **[P-20261110-1] Página de regalos de Navidad (prioridad: es la temporada).**
  https://dulcesmarisol.es/regalos-navidad/ · Ahora el título (70 caracteres) y la
  descripción (166) son tan largos que Google los corta.
  - Título nuevo: «Regalos de Navidad artesanos de Cuenca | Dulces Marisol»
  - Descripción nueva: «Regala dulces manchegos artesanos esta Navidad: surtidos, mantecados,
    rolletes y pastas hechos a mano en Cuenca. Envío 24/48 h, gratis desde 60 €.»
- [ ] **[P-20261110-2] Página «Conócenos».** https://dulcesmarisol.es/conocenos/
  Ahora la descripción solo dice «Obrador de repostería MariSol» y el título es muy corto.
  - Título nuevo: «Nuestro obrador familiar en Cuenca | Dulces Marisol»
  - Descripción nueva: «Conoce Dulces Marisol, obrador familiar de cuarta generación en Cuenca
    que elabora a mano rolletes, mantecados, pastas y magdalenas manchegas.»
- [ ] **[P-20261110-3] Página «Dulces online».** https://dulcesmarisol.es/dulces-online/
  Ahora la descripción es muy corta («Dulces y repostería tradicional de Cuenca»).
  - Descripción nueva: «Compra dulces artesanos de Cuenca online: rolletes, mantecados, pastas,
    magdalenas y surtidos hechos a mano. Envío gratis en península desde 60 €.»
  - Además tiene poco texto (180 palabras). Si te parece bien, propondré un texto de unas
    250 palabras más en otra propuesta.
- [ ] **[P-20261110-4] Título del blog.** https://dulcesmarisol.es/blog-dulces-marisol/
  Ahora tiene 65 caracteres y Google lo corta.
  - Título nuevo: «Blog de dulces manchegos y recetas | Dulces Marisol»

- [ ] **[P-20261111-1] Enlazar la entrada nueva de regalos para empresas.** La entrada
  https://dulcesmarisol.es/regalos-navidad-empresas-dulces-artesanos/ está muy bien, pero
  ninguna página importante enlaza a ella, y así a Google le cuesta encontrarla y darle valor.
  - Añadir al final de la página https://dulcesmarisol.es/regalos-navidad/ esta frase con enlace:
    «¿Buscas regalos para tus clientes o tu equipo? Mira nuestras
    [ideas de regalos de Navidad para empresas](https://dulcesmarisol.es/regalos-navidad-empresas-dulces-artesanos/).»
  - Si prefieres hacerlo tú a mano en WordPress, márcalo igual con [x] cuando esté.

## Tareas para Marisol (se hacen a mano en el panel; aquí solo se marca cuando estén)

- [ ] **[T-20261109-1] Arreglar el acceso del sistema a WordPress.** Tu servidor
  (LiteSpeed) no deja pasar la credencial a WordPress, y sin eso el sistema no puede
  aplicar nada. Pide a tu hosting que añada esta línea al archivo `.htaccess`,
  justo después de `RewriteEngine On`:
  `RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]`
- [ ] **[T-20261109-2] Redirigir 3 páginas que dan error 404** a la tienda. Google
  las encuentra en el sitemap, pero ya no existen (eran vinos):
  `/sin-categoria/teatinos-blanco/`, `/sin-categoria/teatinos-rosado/`,
  `/sin-categoria/teatinos-tempranillo/`.
  Ve a **Rank Math → Redirecciones → Añadir nueva**, pon cada URL de origen y como
  destino `https://dulcesmarisol.es/tienda/`, con tipo **301**. Si esas entradas
  siguen existiendo como borrador o en la papelera, bórralas para que salgan del sitemap.
- [ ] **[T-20261109-3] Redirigir `/comprar-vinos/` a `/tienda/` (301).** Es una
  página antigua con el mismo título y la misma descripción que la tienda, y eso
  confunde a Google. Usa el mismo sitio que en la tarea anterior (Rank Math → Redirecciones).
- [ ] **[T-20261109-4] Sacar del sitemap el carrito, finalizar compra y mi cuenta.**
  Google no debe indexarlas (ya están en "noindex"), pero el sitemap se las sigue
  mostrando. Ve a **Rank Math → Ajustes del sitemap → Páginas → Excluir entradas**
  y añade esas tres páginas.
- [ ] **[T-20261109-5] Marcar la web como pastelería local en Google.** Ve a
  **Rank Math → Títulos y Meta → Local SEO**: tipo de negocio
  **"Bakery" (Panadería/Pastelería)**, dirección del obrador, teléfono y horario.
  Así Google entiende que eres un negocio de Cuenca y no un blog.

- [ ] **[T-20261110-1] Poner una imagen por defecto para cuando se comparte la web.**
  14 páginas (aviso legal, envíos, blog, etc.) no tienen imagen al compartirlas en WhatsApp o
  Facebook. Ve a **Rank Math → Títulos y Meta → Global → Imagen OpenGraph por defecto** y
  elige una foto bonita de vuestros dulces (mejor de 1200 × 630 píxeles).

## Aplicadas

## Rechazadas

## Caducadas
