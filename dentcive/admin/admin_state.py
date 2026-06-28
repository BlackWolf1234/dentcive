"""State del panel de administración.

Permite listar, crear, editar y eliminar productos desde una interfaz web,
persistiendo los cambios directamente en ``products_config.json``.
"""
from __future__ import annotations

import os
from typing import Any

import reflex as rx

from dentcive.admin import products_store
from dentcive.data.products import BRANDS, TAGS, CATEGORIES, SUBCATEGORIES
from dentcive.state import Product, State as PublicState


# La contraseña se carga desde admin_config.json, con fallback a variable
# de entorno DENTCIVE_ADMIN_PASSWORD, y por defecto "2b2".


class AdminState(rx.State):
    """Estado del panel de administración."""

    # ---- Auth ----
    is_admin_authenticated: bool = False
    admin_username_input: str = ""
    admin_password_input: str = ""
    admin_login_error: str = ""
    # Cambio de credenciales
    old_password_input: str = ""
    change_new_username: str = ""
    change_new_password: str = ""
    change_confirm_password: str = ""
    change_phone: str = ""
    sms_code_generated: str = ""
    sms_code_input: str = ""
    sms_step: str = "input"  # "input" | "code_sent" | "verified"
    change_feedback: str = ""
    change_feedback_kind: str = "success"

    # ---- Catálogo en memoria (reflejado del JSON) ----
    products: list[Product] = []
    available_images: list[str] = []

    # ---- PDFs del catálogo ----
    catalog_pdfs: list[dict] = []
    pdf_upload_feedback: str = ""
    pdf_name_input: str = ""
    pdf_delete_feedback: str = ""

    # ---- Formulario ----
    form_id: str = ""
    form_name_es: str = ""
    form_name_en: str = ""
    form_category: str = "repuestos"
    form_price: float = 0.0
    form_old_price: float = 0.0
    form_image: str = ""
    form_description_es: str = ""
    form_description_en: str = ""
    form_badge: str = ""
    form_featured: bool = False
    # Nuevas características: marca (catálogo) y etiqueta (filtrado /servicio-tecnico)
    form_brand: str = ""
    form_tag: str = ""

    # ID del producto en edición (vacío = nuevo)
    editing_id: str = ""
    form_feedback: str = ""
    form_feedback_kind: str = "success"  # "success" | "error"

    # ---- Categorías, badges, marcas y tags disponibles ----
    categories: list[str] = [c["id"] for c in CATEGORIES]
    subcategories: list[str] = [s["id"] for s in SUBCATEGORIES.get("rotatorio", [])]
    badges: list[str] = ["", "SAT", "Servicio", "Asesoría", "Catálogo", "Outlet"]
    # Lista de marcas disponibles para el campo "brand"
    brands: list[str] = BRANDS
    # Lista de IDs de etiquetas disponibles para el campo "tag"
    tags: list[str] = [t["id"] for t in TAGS]
    form_subcategory: str = ""

    # ----------------- Lifecycle -----------------

    async def on_load(self):
        """Carga inicial al entrar a la página /admin."""
        self._reload_catalog()
        self.change_phone = products_store.load_admin_phone()
        ps = await self.get_state(PublicState)
        ps.reload_products()

    def _reload_catalog(self):
        self.products = products_store.load_products()
        self.available_images = products_store.list_images()
        self.catalog_pdfs = products_store.list_pdfs()

    # ----------------- Setters explícitos (Reflex 0.9) -----------------

    def set_admin_username_input(self, value: str):
        self.admin_username_input = value

    def set_admin_password_input(self, value: str):
        self.admin_password_input = value

    def set_form_id(self, value: str):
        self.form_id = value

    def set_form_name_es(self, value: str):
        self.form_name_es = value

    def set_form_name_en(self, value: str):
        self.form_name_en = value

    def set_form_category(self, value: str):
        self.form_category = value

    def set_form_price(self, value):
        try:
            self.form_price = float(value or 0)
        except (TypeError, ValueError):
            self.form_price = 0.0

    def set_form_old_price(self, value):
        try:
            self.form_old_price = float(value or 0)
        except (TypeError, ValueError):
            self.form_old_price = 0.0

    def set_form_image(self, value: str):
        self.form_image = value

    def set_form_description_es(self, value: str):
        self.form_description_es = value

    def set_form_description_en(self, value: str):
        self.form_description_en = value

    def set_form_badge(self, value: str):
        self.form_badge = value

    def set_form_featured(self, value: bool):
        self.form_featured = bool(value)

    def set_form_brand(self, value: str):
        self.form_brand = value

    def set_form_tag(self, value: str):
        self.form_tag = value

    def set_form_subcategory(self, value: str):
        self.form_subcategory = value

    # ----------------- Auth -----------------

    def login_admin(self):
        expected_user = products_store.load_admin_username()
        expected_pass = products_store.load_admin_password()
        if self.admin_username_input == expected_user and self.admin_password_input == expected_pass:
            self.is_admin_authenticated = True
            self.admin_login_error = ""
            self.admin_username_input = ""
            self.admin_password_input = ""
            self._reload_catalog()
        else:
            self.admin_login_error = "Usuario o contraseña incorrectos"

    def logout_admin(self):
        self.is_admin_authenticated = False
        self.admin_username_input = ""
        self.admin_password_input = ""
        self.admin_login_error = ""
        self._reset_change_form()

    def _reset_change_form(self):
        self.old_password_input = ""
        self.change_new_username = ""
        self.change_new_password = ""
        self.change_confirm_password = ""
        self.change_phone = products_store.load_admin_phone()
        self.sms_code_generated = ""
        self.sms_code_input = ""
        self.sms_step = "input"
        self.change_feedback = ""

    def set_old_password_input(self, value: str):
        self.old_password_input = value

    def set_change_new_username(self, value: str):
        self.change_new_username = value

    def set_change_new_password(self, value: str):
        self.change_new_password = value

    def set_change_confirm_password(self, value: str):
        self.change_confirm_password = value

    def set_change_phone(self, value: str):
        self.change_phone = value

    def set_sms_code_input(self, value: str):
        self.sms_code_input = value

    def send_sms_code(self):
        """Verifica la contraseña anterior y envía (simula) un SMS con código."""
        if self.old_password_input != products_store.load_admin_password():
            self.change_feedback = "La contraseña anterior no es correcta"
            self.change_feedback_kind = "error"
            return
        if self.change_new_password and self.change_new_password != self.change_confirm_password:
            self.change_feedback = "Las contraseñas nuevas no coinciden"
            self.change_feedback_kind = "error"
            return
        import random
        self.sms_code_generated = str(random.randint(100000, 999999))
        self.sms_step = "code_sent"
        self.change_feedback = (
            f"Código de verificación enviado al {self.change_phone}: {self.sms_code_generated}"
        )
        self.change_feedback_kind = "success"

    def verify_sms_and_save(self):
        """Verifica el código SMS y guarda los cambios."""
        if self.sms_code_input != self.sms_code_generated:
            self.change_feedback = "Código de verificación incorrecto"
            self.change_feedback_kind = "error"
            return
        if self.change_new_username:
            products_store.save_admin_username(self.change_new_username)
        if self.change_new_password:
            products_store.save_admin_password(self.change_new_password)
        if self.change_phone:
            products_store.save_admin_phone(self.change_phone)
        self.change_feedback = "Credenciales actualizadas correctamente"
        self.change_feedback_kind = "success"
        self.sms_step = "verified"
        self.old_password_input = ""
        self.sms_code_input = ""
        self.sms_code_generated = ""

    # ----------------- PDF Catalog -----------------

    def set_pdf_name_input(self, value: str):
        self.pdf_name_input = value

    async def handle_pdf_upload(self, files: list[rx.UploadFile]):
        if not files:
            return
        uploaded = []
        for f in files:
            if not f.filename.lower().endswith(".pdf"):
                self.pdf_upload_feedback = f"Solo PDFs: {f.filename} ignorado"
                continue
            upload_data = await f.read()
            upload_dir = rx.get_upload_dir()
            upload_dir.mkdir(parents=True, exist_ok=True)
            tmp_path = upload_dir / f.filename
            with open(tmp_path, "wb") as out:
                out.write(upload_data)
            final = products_store.upload_pdf(str(tmp_path), f.filename)
            uploaded.append(final)
            try:
                os.remove(tmp_path)
            except OSError:
                pass
            name = self.pdf_name_input.strip() or os.path.splitext(f.filename)[0]
            pdfs = products_store.list_pdfs()
            pdfs.append({"name": name, "file": final})
            products_store.save_pdfs(pdfs)
            self.pdf_name_input = ""
        self.catalog_pdfs = products_store.list_pdfs()
        self.pdf_upload_feedback = f"Subido: {', '.join(uploaded)}" if uploaded else ""

    async def delete_pdf(self, filename: str):
        products_store.delete_pdf(filename)
        pdfs = [p for p in self.catalog_pdfs if p["file"] != filename]
        products_store.save_pdfs(pdfs)
        self.catalog_pdfs = pdfs
        self.pdf_delete_feedback = f"Eliminado: {filename}"

    # ----------------- Form helpers -----------------

    def _reset_form(self):
        self.editing_id = ""
        empty = products_store.empty_product()
        self.form_id = ""
        self.form_name_es = empty["name"]["es"]
        self.form_name_en = empty["name"]["en"]
        self.form_category = empty["category"]
        self.form_subcategory = empty.get("subcategory", "")
        self.form_price = empty["price"]
        self.form_brand = empty.get("brand", "")
        self.form_tag = empty.get("tag", "")
        self.form_old_price = empty["old_price"]
        self.form_image = empty["image"]
        self.form_description_es = empty["description"]["es"]
        self.form_description_en = empty["description"]["en"]
        self.form_badge = empty["badge"]
        self.form_featured = empty["featured"]
        self.form_feedback = ""

    def start_new_product(self):
        self._reset_form()

    def edit_product(self, product_id: str):
        """Carga los datos de un producto en el formulario a partir de su ID.

        En Reflex 0.9 los handlers deben recibir tipos primitivos serializables,
        no dicts rx.Var. Por eso se pasa el ID y se busca el producto aquí.
        """
        for p in self.products:
            if p.get("id") == product_id:
                self.editing_id = product_id
                self.form_id = product_id
                self.form_name_es = p.get("name", {}).get("es", "")
                self.form_name_en = p.get("name", {}).get("en", "")
                self.form_brand = p.get("brand", "") or ""
                self.form_tag = p.get("tag", "") or ""
                self.form_subcategory = p.get("subcategory", "") or ""
                self.form_category = p.get("category", "ofertas")
                self.form_price = float(p.get("price", 0))
                self.form_old_price = float(p.get("old_price", 0))
                self.form_image = p.get("image", "")
                self.form_description_es = p.get("description", {}).get("es", "")
                self.form_description_en = p.get("description", {}).get("en", "")
                self.form_badge = p.get("badge", "")
                self.form_featured = bool(p.get("featured", False))
                self.form_feedback = ""
                return

    async def delete_product(self, product_id: str):
        self.products = [p for p in self.products if p.get("id") != product_id]
        products_store.save_products(self.products)
        if self.editing_id == product_id:
            self._reset_form()
        ps = await self.get_state(PublicState)
        ps.reload_products()
        self._flash("Producto eliminado", "success")

    # ----------------- Save -----------------

    async def save_product(self):
        # Validación
        if not self.form_name_es.strip():
            self._flash("El nombre en español es obligatorio", "error")
            return
        if not self.form_image.strip():
            self._flash("Selecciona una imagen", "error")
            return

        if self.editing_id:
            target_id = self.editing_id
        else:
            target_id = products_store.next_product_id(self.products)
        new_product = {
            "id": target_id,
            "name": {"es": self.form_name_es.strip(), "en": self.form_name_en.strip()},
            "category": self.form_category,
            "subcategory": self.form_subcategory,
            "price": float(self.form_price),
            "old_price": float(self.form_old_price),
            "image": self.form_image,
            "description": {
                "es": self.form_description_es.strip(),
                "en": self.form_description_en.strip(),
            },
            "badge": self.form_badge,
            "featured": bool(self.form_featured),
            "brand": self.form_brand.strip(),
            "tag": self.form_tag.strip(),
        }

        if self.editing_id:
            self.products = [
                new_product if p.get("id") == self.editing_id else p
                for p in self.products
            ]
            self._flash(f"Producto {target_id} actualizado", "success")
        else:
            self.products = [*self.products, new_product]
            self._flash(f"Producto {target_id} creado", "success")

        products_store.save_products(self.products)
        self.editing_id = target_id
        self.form_id = target_id
        # Sincronizar catálogo público para que se vea al instante
        ps = await self.get_state(PublicState)
        ps.reload_products()

    # ----------------- Upload -----------------

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Recibe uno o varios archivos subidos y los copia a /public."""
        if not files:
            return
        uploaded = []
        for f in files:
            upload_data = await f.read()
            upload_dir = rx.get_upload_dir()
            upload_dir.mkdir(parents=True, exist_ok=True)
            tmp_path = upload_dir / f.filename
            with open(tmp_path, "wb") as out:
                out.write(upload_data)
            final_name = products_store.upload_image(str(tmp_path), f.filename)
            uploaded.append(final_name)
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        self.available_images = products_store.list_images()
        if uploaded:
            self.form_image = uploaded[0]
            self._flash(
                f"Subida: {', '.join(uploaded)}. Recuerda pulsar Guardar.",
                "success",
            )

    # ----------------- Feedback -----------------

    def _flash(self, msg: str, kind: str):
        self.form_feedback = msg
        self.form_feedback_kind = kind