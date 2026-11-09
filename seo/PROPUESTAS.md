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

## Aplicadas

## Rechazadas

## Caducadas
