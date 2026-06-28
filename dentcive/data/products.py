import json
import os

from dentcive.admin.products_store import _enrich_product

# ---- Carga del catálogo ----

config_path = os.path.join(os.path.dirname(__file__), "products_config.json")


try:
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
        PRODUCTS = [_enrich_product(p) for p in config.get("products", [])]
except FileNotFoundError:
    # Fallback si no existe el archivo JSON
    PRODUCTS = []

CATEGORIES = [
    {"id": "ofertas", "name": {"es": "Ofertas", "en": "Offers"}, "icon": "badge-euro"},
    {"id": "equipos", "name": {"es": "Equipos", "en": "Equipment"}, "icon": "monitor-cog"},
    {"id": "compresores", "name": {"es": "Compresores", "en": "Compressors"}, "icon": "wind"},
    {"id": "aspiraciones", "name": {"es": "Aspiraciones", "en": "Suctions"}, "icon": "vacuum"},
    {"id": "autoclaves", "name": {"es": "Autoclaves", "en": "Autoclaves"}, "icon": "thermometer"},
    {"id": "selladoras", "name": {"es": "Selladoras", "en": "Sealers"}, "icon": "container"},
    {"id": "ultrasonidos", "name": {"es": "Ultrasonidos", "en": "Ultrasounds"}, "icon": "radio"},
    {"id": "rotatorio", "name": {"es": "Rotatorio", "en": "Rotary"}, "icon": "rotate-cw"},
]

SUBCATEGORIES = {
    "rotatorio": [
        {"id": "turbina", "name": {"es": "Turbina", "en": "Turbine"}},
        {"id": "contra-angulos", "name": {"es": "Contra-Ángulos", "en": "Contra-Angles"}},
        {"id": "pieza-mano", "name": {"es": "Pieza de Mano", "en": "Handpiece"}},
        {"id": "jeringa", "name": {"es": "Jeringa Agua/Aire", "en": "Water/Air Syringe"}},
        {"id": "micromotores", "name": {"es": "Micromotores", "en": "Micromotors"}},
    ],
}

COUPONS = [
    {"code": "DENTAL10", "discount": 10, "description_es": "10% descuento", "description_en": "10% off"},
    {"code": "PROMO20", "discount": 20, "description_es": "20% descuento", "description_en": "20% off"},
    {"code": "WELCOME", "discount": 5, "description_es": "Bienvenida 5%", "description_en": "Welcome 5%"},
]

BRANDS = [
    "Bien Air", "Mectron", "LM", "VOCO", "Dentsply", "3M",
    "Ivoclar", "Dentalez", "NSK", "KAVO", "Sirona",
]

# Etiquetas para clasificar productos (además de la "badge" visual).
# Se usa para filtrar la página /servicio-tecnico (tag == "servicio").
TAGS = [
    {"id": "", "label": "— Ninguna —"},
    {"id": "servicio", "label": "Servicio técnico"},
    {"id": "venta", "label": "Venta"},
    {"id": "reparacion", "label": "Reparación"},
    {"id": "asistencia", "label": "Asistencia"},
    {"id": "repuesto", "label": "Repuesto"},
]

# Producto se considera de "servicio técnico" si tiene badge "Servicio"
# o si su tag es "servicio".
def is_service_product(p: dict) -> bool:
    """True si el producto pertenece al servicio técnico."""
    return p.get("badge") == "Servicio" or p.get("tag") == "servicio"


def list_service_products() -> list[dict]:
    """Devuelve los productos de servicio técnico a partir de PRODUCTS."""
    return [p for p in PRODUCTS if is_service_product(p)]
