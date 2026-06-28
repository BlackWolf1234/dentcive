# Cómo Agregar Productos a Dentcive

Tienes dos opciones. **Recomendamos el panel web** porque gestiona todo (incluida la subida de imágenes) sin tocar archivos.

---

## 🌐 Opción 1: Panel de administración (RECOMENDADA)

1. Ve a `http://localhost:3000/admin`
2. Introduce la contraseña (por defecto: `admin1234`)
3. Pulsa **Nuevo** o **Editar** sobre uno existente
4. Rellena los campos:
   - Nombre ES / EN
   - Categoría (`clinic`, `laboratorio`, `estudiantes`, `repuestos`, `equipamiento`, `consumibles`)
   - Precio y precio anterior
   - Imagen: elige una de `/public/` o sube una nueva
   - Descripción ES / EN
   - Badge (`SAT`, `Servicio`, `Asesoría`, `Catálogo`, `Outlet`, o vacío)
   - Marca **Destacado** si quieres que aparezca primero
5. Pulsa **Crear producto** o **Actualizar**
6. Ejecuta el rebuild para que aparezca en la landing:
   ```bash
   reflex export --frontend-only && unzip -o frontend.zip -d public && rm frontend.zip
   ```

---

## ✏️ Opción 2: Editar `products_config.json` directamente

1. Abre `dentcive/data/products_config.json`
2. Añade un objeto al array `"products"`:

```json
{
  "id": "prod_005",
  "name": {"es": "Nombre en español", "en": "Name in English"},
  "category": "repuestos",
  "price": 150.00,
  "old_price": 200.00,
  "image": "mi-imagen.png",
  "description": {"es": "Descripción en español", "en": "Description in English"},
  "badge": "SAT",
  "featured": true
}
```

3. Coloca la imagen en `public/`
4. Regenera el build

---

## 📸 Cómo Agregar Imágenes

### Desde el panel admin
Usa el botón **Subir imagen** del formulario. El archivo se guarda automáticamente en `/public/` y se selecciona como imagen del producto.

### Manualmente
Copia el archivo (PNG, JPG, WebP) a la carpeta `public/` y referencia el nombre en `"image"` del JSON.

### Tamaños recomendados
| | |
|---|---|
| **Ancho** | 400 – 600 px |
| **Alto** | 300 – 400 px |
| **Formato** | PNG, JPG, WebP |

---

## 🏷️ Categorías disponibles

- `clinic` - Clínica
- `laboratorio` - Laboratorio
- `estudiantes` - Estudiantes
- `repuestos` - Repuestos
- `equipamiento` - Equipamiento
- `consumibles` - Consumibles

## ✨ Badges disponibles

- `SAT` - Servicio de Asistencia Técnica
- `Servicio` - Servicio técnico
- `Asesoría` - Asesoramiento comercial
- `Catálogo` - Catálogo general
- `Outlet` - En oferta
- Vacío `""` para sin badge

---

**Los cambios del panel se guardan al instante en `products_config.json`.** Recuerde hacer rebuild para que aparezcan en la landing pública.