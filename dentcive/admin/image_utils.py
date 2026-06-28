"""Utilidades para ajustar y optimizar las imágenes de productos.

Cuando se sube una imagen al panel admin, se procesa automáticamente:
  - Se redimensiona manteniendo proporción hasta un máximo (ancho y alto).
  - Se centra sobre un lienzo del tamaño final (rellenando con blanco).
  - Se guarda como JPG calidad 85 (mucho más liviano que PNG original).

Si Pillow no está disponible, se hace un fallback a copia directa sin tocar.
"""
from __future__ import annotations

import os
from typing import Tuple

# Tamaño final de las imágenes de producto. Coincide con el alto del
# contenedor en product_card (170px) usando una proporción 4:3 para que
# se vean bien al recortar con object-fit: cover.
TARGET_SIZE: Tuple[int, int] = (1200, 900)
JPEG_QUALITY: int = 85


def is_pillow_available() -> bool:
    """Devuelve True si Pillow está instalado y operativo."""
    try:
        from PIL import Image  # noqa: F401
        return True
    except ImportError:
        return False


def process_product_image(src_path: str, dest_path: str) -> str:
    """Ajusta ``src_path`` y guarda el resultado en ``dest_path``.

    Pasos:
      1. Abre la imagen original.
      2. Redimensiona manteniendo proporción para que quepa en TARGET_SIZE.
      3. Centra sobre un lienzo del tamaño final (fondo blanco).
      4. Guarda como JPG con calidad JPEG_QUALITY.

    Args:
        src_path: Ruta absoluta de la imagen original.
        dest_path: Ruta absoluta del archivo final. Si termina en ``.png`` o
                   ``.webp`` se cambia a ``.jpg``.

    Returns:
        Ruta absoluta del archivo escrito.
    """
    if not is_pillow_available():
        # Sin Pillow: copiamos tal cual
        import shutil
        shutil.copy2(src_path, dest_path)
        return dest_path

    from PIL import Image

    # Cambiar extensión a .jpg para optimizar
    base, _ = os.path.splitext(dest_path)
    final_path = base + ".jpg"
    if dest_path != final_path and os.path.exists(dest_path):
        try:
            os.remove(dest_path)
        except OSError:
            pass

    with Image.open(src_path) as img:
        # Convertir paletas/modos raros a RGB para poder guardar como JPG
        if img.mode in ("RGBA", "LA", "P"):
            # Para PNGs con transparencia: aplanar sobre fondo blanco
            bg = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            bg.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
            img = bg
        elif img.mode != "RGB":
            img = img.convert("RGB")

        # Redimensionar manteniendo proporción (thumbnail NO agranda)
        img.thumbnail(TARGET_SIZE, Image.Resampling.LANCZOS)

        # Centrar sobre un lienzo del tamaño final
        canvas = Image.new("RGB", TARGET_SIZE, (255, 255, 255))
        x = (TARGET_SIZE[0] - img.width) // 2
        y = (TARGET_SIZE[1] - img.height) // 2
        canvas.paste(img, (x, y))

        # Guardar como JPG optimizado
        canvas.save(final_path, "JPEG", quality=JPEG_QUALITY, optimize=True)

    return final_path