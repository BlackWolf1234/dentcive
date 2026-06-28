"""Capa de persistencia del catálogo de productos.

Lee y escribe ``dentcive/data/products_config.json``. Mantiene la lista
de productos en memoria y la sincroniza con disco al guardar.
"""
from __future__ import annotations

import json
import os
from urllib.parse import quote
from typing import Any

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "products_config.json",
)
PUBLIC_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "public",
)

# Campos calculados que se añaden en memoria y NO deben persistirse en el JSON
_COMPUTED_FIELDS = {"price_str", "old_price_str", "wa_url", "budget_url", "brand_or_empty", "tag_or_empty"}

_WHATSAPP_NUMBER = "34661921722"
_WA_PREFIX = "https://wa.me/" + _WHATSAPP_NUMBER + "?text=" + quote("Hola, quiero informacion sobre ")


def _enrich_product(p: dict) -> dict:
    """Añade campos calculados a un dict de producto.

    Estos campos son necesarios para renderizar la tarjeta de producto con
    ``rx.foreach`` de Reflex, donde los valores son ``rx.Var`` y no soportan
    f-strings con especificadores de formato.
    """
    price = float(p.get("price", 0))
    old_price = float(p.get("old_price", 0))
    name_es = p.get("name", {}).get("es", "")
    subject = quote(f"Solicitud de presupuesto: {name_es}")
    return {
        **p,
        "price_str": f"${price:.2f}",
        "old_price_str": f"${old_price:.2f}" if old_price > 0 else "",
        "wa_url": _WA_PREFIX + quote(name_es),
        "budget_url": f"mailto:dentcive@gmail.com?subject={subject}",
        "brand_or_empty": p.get("brand", "") or "",
        "tag_or_empty": p.get("tag", "") or "",
    }


def load_products() -> list[dict]:
    """Lee el catálogo desde disco y enriquece cada producto con campos calculados.

    Devuelve lista vacía si el archivo no existe.
    """
    if not os.path.exists(CONFIG_PATH):
        return []
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [_enrich_product(p) for p in data.get("products", [])]


def save_products(products: list[dict]) -> None:
    """Persiste el catálogo en disco eliminando los campos calculados antes de escribir."""
    # Eliminar campos calculados para no contaminar el JSON fuente
    clean = [
        {k: v for k, v in p.items() if k not in _COMPUTED_FIELDS}
        for p in products
    ]
    payload = {
        "products": clean,
        "instructions": (
            "Para agregar un nuevo producto, copia este formato y añádelo al "
            "array 'products'. Las imágenes deben estar en /public/"
        ),
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def list_images() -> list[str]:
    """Lista todas las imágenes disponibles en /public para usar en formularios."""
    if not os.path.isdir(PUBLIC_DIR):
        return []
    valid_ext = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
    images = []
    for fname in sorted(os.listdir(PUBLIC_DIR)):
        full = os.path.join(PUBLIC_DIR, fname)
        if os.path.isfile(full) and os.path.splitext(fname)[1].lower() in valid_ext:
            images.append(fname)
    return images


def upload_image(src_path: str, target_name: str | None = None) -> str:
    """Ajusta una imagen subida y la guarda en /public/ como JPG optimizado.

    Args:
        src_path: Ruta absoluta del archivo origen.
        target_name: Nombre destino. Si no se da, se usa el basename del origen.

    Returns:
        Nombre final del archivo en /public/ (con extensión .jpg).

    Raises:
        FileNotFoundError: Si el archivo origen no existe.
    """
    from dentcive.admin.image_utils import process_product_image

    if not os.path.isfile(src_path):
        raise FileNotFoundError(f"No existe: {src_path}")
    final_name = target_name or os.path.basename(src_path)
    # Forzar extensión .jpg para optimizar peso
    base, _ext = os.path.splitext(final_name)
    final_name = base + ".jpg"
    dest = os.path.join(PUBLIC_DIR, final_name)
    # Procesar imagen (redimensionar + centrar + convertir a JPG)
    final_dest = process_product_image(src_path, dest)
    return os.path.basename(final_dest)


# ---------------------------------------------------------------------------
# Admin password persistence
# ---------------------------------------------------------------------------

ADMIN_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "admin_config.json",
)


ADMIN_USERNAME = "JefferCanizar"


def _load_admin_config() -> dict:
    """Lee el archivo de configuración del admin o devuelve dict vacío."""
    if os.path.exists(ADMIN_CONFIG_PATH):
        try:
            with open(ADMIN_CONFIG_PATH, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_admin_config(data: dict) -> None:
    """Escribe el archivo de configuración del admin."""
    with open(ADMIN_CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)


def load_admin_username() -> str:
    """Carga el usuario del admin.
    Fallback: variable de entorno DENTCIVE_ADMIN_USERNAME, luego "JefferCanizar".
    """
    env_username = os.environ.get("DENTCIVE_ADMIN_USERNAME")
    if env_username:
        return env_username
    data = _load_admin_config()
    return data.get("admin_username", "") or ADMIN_USERNAME


def save_admin_username(username: str) -> None:
    """Persiste el usuario del admin."""
    data = _load_admin_config()
    data["admin_username"] = username
    _save_admin_config(data)


def load_admin_password() -> str:
    """Carga la contraseña del admin desde el archivo de configuración.
    Fallback: variable de entorno DENTCIVE_ADMIN_PASSWORD, luego "2b2".
    """
    env_password = os.environ.get("DENTCIVE_ADMIN_PASSWORD")
    if env_password:
        return env_password
    data = _load_admin_config()
    pwd = data.get("admin_password", "")
    return pwd if pwd else "2b2"


def save_admin_password(password: str) -> None:
    """Persiste la contraseña del admin en el archivo de configuración."""
    data = _load_admin_config()
    data["admin_password"] = password
    _save_admin_config(data)


def load_admin_phone() -> str:
    """Carga el teléfono asociado para SMS.
    Fallback: variable de entorno DENTCIVE_ADMIN_PHONE, luego "+34 661 921 722".
    """
    env_phone = os.environ.get("DENTCIVE_ADMIN_PHONE")
    if env_phone:
        return env_phone
    data = _load_admin_config()
    return data.get("admin_phone", "") or "+34 661 921 722"


def save_admin_phone(phone: str) -> None:
    """Persiste el teléfono asociado para SMS."""
    data = _load_admin_config()
    data["admin_phone"] = phone
    _save_admin_config(data)


def next_product_id(products: list[dict]) -> str:
    """Genera un ID correlativo para el próximo producto (prod_005, prod_006, ...)."""
    nums = []
    for p in products:
        pid = p.get("id", "")
        if pid.startswith("prod_"):
            try:
                nums.append(int(pid.split("_", 1)[1]))
            except ValueError:
                pass
    nxt = (max(nums) + 1) if nums else 1
    return f"prod_{nxt:03d}"


# ---------------------------------------------------------------------------
# PDF catalog management
# ---------------------------------------------------------------------------

CATALOG_PDFS_CONFIG = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "catalog_pdfs.json",
)

PDF_CATALOG_DIR = PUBLIC_DIR


def list_pdfs() -> list[dict]:
    """Lista los PDFs del catálogo desde el JSON de configuración."""
    if not os.path.exists(CATALOG_PDFS_CONFIG):
        return []
    with open(CATALOG_PDFS_CONFIG, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("pdfs", [])


def save_pdfs(pdfs: list[dict]) -> None:
    """Persiste la lista de PDFs del catálogo."""
    payload = {"pdfs": pdfs}
    with open(CATALOG_PDFS_CONFIG, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def upload_pdf(src_path: str, filename: str) -> str:
    """Copia un PDF a /public/."""
    dest = os.path.join(PDF_CATALOG_DIR, filename)
    with open(src_path, "rb") as src:
        with open(dest, "wb") as dst:
            dst.write(src.read())
    return filename


def delete_pdf(filename: str) -> None:
    """Elimina un PDF de /public/."""
    path = os.path.join(PDF_CATALOG_DIR, filename)
    try:
        os.remove(path)
    except OSError:
        pass


def empty_product() -> dict[str, Any]:
    """Devuelve la plantilla de un producto nuevo para inicializar formularios."""
    return {
        "id": "",
        "name": {"es": "", "en": ""},
        "category": "repuestos",
        "price": 0.0,
        "old_price": 0.0,
        "image": "",
        "description": {"es": "", "en": ""},
        "badge": "",
        "featured": False,
        "brand": "",
        "tag": "",
        "subcategory": "",
    }