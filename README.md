# Dentcive

Catálogo web para clínica dental con **Reflex** (Python → React).

## Características

- Landing pública (`/`) con catálogo, hero, servicios y contacto
- Panel de administración (`/admin`) para gestionar productos desde la web
- Soporte bilingüe (ES / EN)
- Catálogo persistido en `dentcive/data/products_config.json`
- Imágenes servidas desde `public/`

## Estructura del proyecto

```
dentcive/
├── assets/                     # Recursos de marca (logos, hero bg)
├── build.sh                    # Build de producción (export + unzip)
├── requirements.txt
├── rxconfig.py                 # Config de Reflex
├── COMO_AGREGAR_PRODUCTOS.md   # Guía legacy para editar JSON a mano
├── dentcive/                   # Código fuente
│   ├── dentcive.py             # Entry point + registro de rutas
│   ├── state.py                # State global (auth, cart, wishlist, productos)
│   ├── admin/                  # Panel de administración
│   │   ├── admin_page.py       # UI (login + dashboard + formulario)
│   │   ├── admin_state.py      # State del admin (CRUD en memoria)
│   │   └── products_store.py   # Capa de persistencia (lee/escribe JSON)
│   ├── components/             # Componentes reutilizables
│   │   ├── navbar.py
│   │   ├── footer.py
│   │   ├── product_card.py
│   │   ├── cart_modal.py
│   │   └── ...
│   ├── data/
│   │   ├── products.py         # CATEGORIES, COUPONS, BRANDS
│   │   └── products_config.json  # Catálogo (única fuente de verdad)
│   ├── styles/                 # colors, fonts, styles
│   ├── utils/i18n.py           # Helper de traducciones
│   └── views/
│       ├── header/header.py    # Hero + 4 service tiles
│       └── links/links.py      # Catálogo + categorías + contacto
├── public/                     # Build estática generada por reflex export
└── uploaded_files/             # Directorio temporal para uploads (no commitear)
```

## Rutas

| Ruta | Acceso | Descripción |
|---|---|---|
| `/` | público | Landing con catálogo |
| `/admin` | contraseña | Panel CRUD de productos |

## Acceso al panel admin

1. Abre `http://localhost:3000/admin` (o el host configurado)
2. Contraseña por defecto: `admin1234`
3. Para cambiarla, exporta la variable de entorno:
   ```bash
   export DENTCIVE_ADMIN_PASSWORD="tu-contraseña-segura"
   ```

## Desarrollo

```bash
# Crear venv e instalar deps
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Modo dev (hot reload)
reflex run
# Abre http://localhost:3000

# Build de producción
reflex export --frontend-only
unzip -o frontend.zip -d public
rm frontend.zip

# Servir build estática local
cd public && python -m http.server 8088
# Abre http://localhost:8088
```

## Añadir productos

### Opción A: desde el panel web (recomendado)

1. Entra a `/admin` con la contraseña
2. Pulsa **Nuevo** o **Editar** en uno existente
3. Rellena nombre (ES/EN), categoría, precio, imagen, descripción
4. **Sube la imagen** directamente desde el formulario, o elige una de `/public/`
5. Pulsa **Crear producto** / **Actualizar**
6. Ejecuta el rebuild para que aparezca en la landing:
   ```bash
   reflex export --frontend-only && unzip -o frontend.zip -d public && rm frontend.zip
   ```

### Opción B: editar el JSON directamente

Edita `dentcive/data/products_config.json` añadiendo un objeto al array `products`:

```json
{
  "id": "prod_005",
  "name": {"es": "...", "en": "..."},
  "category": "repuestos",
  "price": 100.00,
  "old_price": 0.00,
  "image": "mi-imagen.png",
  "description": {"es": "...", "en": "..."},
  "badge": "SAT",
  "featured": false
}
```

Después regenera el build.

## Imágenes

Las imágenes se sirven desde `public/` (carpeta raíz). Formatos soportados:
`.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`.

Tamaño recomendado: 400-600 px de ancho, 300-400 px de alto.

Cuando subes una imagen desde el panel admin, se copia automáticamente
a `public/` y se selecciona como imagen del producto.