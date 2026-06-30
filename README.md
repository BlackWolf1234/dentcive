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
├── public/                     # Build estática (incluye .nojekyll y /dentcive/)
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
touch public/.nojekyll
# El sitio queda en public/dentcive/
rm frontend.zip

# Servir build estática local
cd public && python -m http.server 8088
# Abre http://localhost:8088
```

## Publicar en producción (GitHub Pages)

Este repositorio ya incluye el workflow
`.github/workflows/deploy-pages.yml`
para publicar la web automáticamente en GitHub Pages.

La app está configurada para publicarse en el subpath `/<repo-name>/`
(`https://<username>.github.io/<repo-name>/` o dominio personalizado).

### 1) Activar Pages en GitHub

1. Ve a **Settings → Pages** del repositorio
2. En **Build and deployment**, selecciona **GitHub Actions**

### 2) Publicación automática

- Cada push a `main` ejecuta el workflow
- El workflow genera el build estático con `reflex export`
- Publica el contenido de `public/` en GitHub Pages (la app queda en `public/dentcive/`)

### 3) Dominio personalizado (opcional)

1. En **Settings → Pages**, agrega tu dominio en **Custom domain**
2. Crea el registro DNS correspondiente:
   - `CNAME` (subdominio) o
   - `A/AAAA` (dominio raíz, según tu proveedor)
3. Activa **Enforce HTTPS** cuando aparezca disponible

### 4) Flujo para actualizar la web

Cada vez que cambies productos o contenido:

1. Haz commit de tus cambios
2. Haz push a `main`
3. Espera a que termine el workflow de Pages

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
