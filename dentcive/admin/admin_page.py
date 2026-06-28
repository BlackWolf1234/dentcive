"""UI del panel de administración (/admin)."""
from __future__ import annotations

import reflex as rx

from dentcive.admin.admin_state import AdminState
from dentcive.styles.colors import Color as Color
from dentcive.styles.colors import TextColor as TextColor
from dentcive.styles.styles import Size as Size
import dentcive.styles.styles as styles


# ------------------------------------------------------------------ helpers

def _section_title(text: str) -> rx.Component:
    return rx.heading(
        text,
        size="5",
        color=TextColor.HEADER.value,
        margin_bottom=Size.DEFAULT.value,
    )


def _field_label(text: str) -> rx.Component:
    return rx.text(
        text,
        font_weight="600",
        font_size="0.9em",
        color=TextColor.BODY.value,
        margin_bottom="0.25em",
    )


def _field(helper_text: str, control: rx.Component) -> rx.Component:
    return rx.vstack(
        helper_text,
        control,
        align_items="stretch",
        spacing="1",
        width="100%",
    )


# ------------------------------------------------------------------ login

def _login_screen() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("🔒 Panel de administración", size="6", color=TextColor.HEADER.value),
            rx.text(
                "Introduce usuario y contraseña para gestionar el catálogo.",
                color=TextColor.BODY.value,
            ),
            rx.text(
                "Usuario: JefferCanizar | Contraseña: 2b2",
                color=TextColor.FOOTER.value,
                font_size="0.85em",
            ),
            rx.input(
                placeholder="Usuario",
                value=AdminState.admin_username_input,
                on_change=AdminState.set_admin_username_input,
                width="100%",
                size="3",
            ),
            rx.input(
                placeholder="Contraseña",
                type="password",
                value=AdminState.admin_password_input,
                on_change=AdminState.set_admin_password_input,
                width="100%",
                size="3",
            ),
            rx.cond(
                AdminState.admin_login_error != "",
                rx.text(AdminState.admin_login_error, color=Color.SALE.value, font_size="0.9em"),
                rx.fragment(),
            ),
            rx.button("Entrar", on_click=AdminState.login_admin, size="3", width="100%"),
            spacing="3",
            width="100%",
            max_width="420px",
            padding="2em",
            background_color=Color.CONTENT.value,
            border=f"1px solid {Color.BORDER.value}",
            border_radius="8px",
        ),
        min_height="80vh",
        padding="2em",
    )


# ------------------------------------------------------------------ form

def _product_form() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading(
                rx.cond(
                    AdminState.editing_id != "",
                    f"✏️ Editando {AdminState.editing_id}",
                    "➕ Nuevo producto",
                ),
                size="5",
                color=TextColor.HEADER.value,
            ),
            rx.spacer(),
            rx.button(
                "Cancelar",
                on_click=AdminState.start_new_product,
                size="2",
                background_color="transparent",
                color=TextColor.BODY.value,
                border=f"1px solid {Color.BORDER.value}",
            ),
            width="100%",
            align="center",
        ),
        rx.grid(
            # Nombre ES / EN
            _field(
                "Nombre (ES)",
                rx.input(
                    placeholder="Reparación de turbina dental",
                    value=AdminState.form_name_es,
                    on_change=AdminState.set_form_name_es,
                    width="100%",
                ),
            ),
            _field(
                "Nombre (EN)",
                rx.input(
                    placeholder="Dental turbine repair",
                    value=AdminState.form_name_en,
                    on_change=AdminState.set_form_name_en,
                    width="100%",
                ),
            ),
            columns=rx.breakpoints(initial="1", md="2"),
            spacing="3",
            width="100%",
        ),
        rx.grid(
            _field(
                "Categoría",
                rx.select(
                    AdminState.categories,
                    value=AdminState.form_category,
                    on_change=AdminState.set_form_category,
                    width="100%",
                ),
            ),
            _field(
                "Subcategoría (Rotatorio)",
                rx.select(
                    AdminState.subcategories,
                    value=AdminState.form_subcategory,
                    on_change=AdminState.set_form_subcategory,
                    width="100%",
                ),
            ),
            _field(
                "Badge",
                rx.select(
                    AdminState.badges,
                    value=AdminState.form_badge,
                    on_change=AdminState.set_form_badge,
                    width="100%",
                ),
            ),
            _field(
                "Precio (€)",
                rx.input(
                    type="number",
                    step="0.01",
                    value=AdminState.form_price.to_string(),
                    on_change=AdminState.set_form_price,
                    width="100%",
                ),
            ),
            _field(
                "Precio anterior (€)",
                rx.input(
                    type="number",
                    step="0.01",
                    value=AdminState.form_old_price.to_string(),
                    on_change=AdminState.set_form_old_price,
                    width="100%",
                ),
            ),
            columns=rx.breakpoints(initial="1", sm="2", md="4"),
            spacing="3",
            width="100%",
        ),
        # Imagen: selector + subida
        _field(
            "Imagen",
            rx.vstack(
                rx.hstack(
                    rx.select(
                        AdminState.available_images,
                        placeholder="Selecciona una imagen…",
                        value=AdminState.form_image,
                        on_change=AdminState.set_form_image,
                        width="100%",
                    ),
                    rx.upload(
                        rx.button(
                            rx.icon(tag="upload", size=16),
                            "Subir imagen",
                            size="2",
                            type="button",
                        ),
                        id="img_upload",
                        multiple=True,
                        accept={
                            "image/png": [".png"],
                            "image/jpeg": [".jpg", ".jpeg"],
                            "image/webp": [".webp"],
                        },
                        on_drop=AdminState.handle_upload(
                            rx.upload_files(upload_id="img_upload")
                        ),
                        width="auto",
                    ),
                    width="100%",
                    spacing="2",
                ),
                rx.cond(
                    AdminState.form_image != "",
                    rx.hstack(
                        rx.text("Vista previa:", font_size="0.85em", color=TextColor.FOOTER.value),
                        rx.image(
                            src=AdminState.form_image,
                            height="60px",
                            width="auto",
                            border_radius="4px",
                            border=f"1px solid {Color.BORDER.value}",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.fragment(),
                ),
                spacing="2",
                width="100%",
            ),
        ),
        rx.grid(
            _field(
                "Descripción (ES)",
                rx.text_area(
                    placeholder="Diagnóstico y reparación con repuestos de máxima calidad.",
                    value=AdminState.form_description_es,
                    on_change=AdminState.set_form_description_es,
                    width="100%",
                    rows="3",
                ),
            ),
            _field(
                "Descripción (EN)",
                rx.text_area(
                    placeholder="Diagnosis and repair with highest quality parts.",
                    value=AdminState.form_description_en,
                    on_change=AdminState.set_form_description_en,
                    width="100%",
                    rows="3",
                ),
            ),
            columns=rx.breakpoints(initial="1", md="2"),
            spacing="3",
            width="100%",
        ),
        rx.hstack(
            rx.checkbox(
                "Destacado (featured)",
                checked=AdminState.form_featured,
                on_change=AdminState.set_form_featured,
            ),
            rx.spacer(),
            rx.button(
                rx.icon(tag="save", size=16),
                rx.cond(AdminState.editing_id != "", "Actualizar", "Crear producto"),
                on_click=AdminState.save_product,
                size="3",
            ),
            spacing="3",
            width="100%",
            align="center",
        ),
        rx.cond(
            AdminState.form_feedback != "",
            rx.callout(
                AdminState.form_feedback,
                icon=rx.cond(
                    AdminState.form_feedback_kind == "success",
                    "check",
                    "alert-triangle",
                ),
                color_scheme=rx.cond(
                    AdminState.form_feedback_kind == "success",
                    "green",
                    "red",
                ),
                width="100%",
            ),
            rx.fragment(),
        ),
        spacing="4",
        width="100%",
        padding="1.5em",
        background_color=Color.CONTENT.value,
        border=f"1px solid {Color.BORDER.value}",
        border_radius="8px",
    )


# ------------------------------------------------------------------ lista

def _product_row(product: dict) -> rx.Component:
    pid = product["id"]
    return rx.hstack(
        rx.image(
            src=product["image"],
            height="40px",
            width="40px",
            object_fit="cover",
            border_radius="4px",
        ),
        rx.vstack(
            rx.text(product["name"]["es"], font_weight="700", color=TextColor.HEADER.value),
            rx.text(
                f"{pid} · {product['category']} · {product['price']}€",
                font_size="0.8em",
                color=TextColor.FOOTER.value,
            ),
            align_items="start",
            spacing="0",
        ),
        rx.spacer(),
        rx.button(
            rx.icon(tag="pencil", size=14),
            "Editar",
            size="1",
            variant="soft",
            on_click=lambda pid=pid: AdminState.edit_product(pid),
        ),
        rx.button(
            rx.icon(tag="trash-2", size=14),
            size="1",
            color_scheme="red",
            variant="soft",
            on_click=lambda x=pid: AdminState.delete_product(x),
        ),
        width="100%",
        padding="0.75em",
        align="center",
        spacing="3",
        border_bottom=f"1px solid {Color.BORDER.value}",
    )


def _products_list() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            _section_title(f"Catálogo ({AdminState.products.length()})"),
            rx.spacer(),
            rx.button(
                rx.icon(tag="plus", size=16),
                "Nuevo",
                on_click=AdminState.start_new_product,
                size="2",
            ),
            width="100%",
            align="center",
        ),
        rx.cond(
            AdminState.products.length() > 0,
            rx.box(
                rx.foreach(AdminState.products, lambda p: _product_row(p)),
                border=f"1px solid {Color.BORDER.value}",
                border_radius="8px",
                background_color=Color.CONTENT.value,
                overflow="hidden",
                width="100%",
            ),
            rx.callout(
                "No hay productos todavía. Crea el primero con el botón 'Nuevo'.",
                icon="info",
                width="100%",
            ),
        ),
        spacing="3",
        width="100%",
    )


# ------------------------------------------------------------------ topbar

def _admin_topbar() -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.image(src="dentcive-logo-retina.png", height="32px", width="auto"),
            rx.text("Admin", font_weight="700", color=TextColor.HEADER.value),
            spacing="3",
            align="center",
        ),
        rx.spacer(),
        rx.hstack(
            rx.link(
                rx.button("← Ver web", size="2", variant="soft"),
                href="/",
            ),
            rx.button(
                rx.icon(tag="log-out", size=14),
                "Salir",
                size="2",
                variant="soft",
                color_scheme="red",
                on_click=AdminState.logout_admin,
            ),
            spacing="2",
        ),
        width="100%",
        padding="1em 2em",
        border_bottom=f"1px solid {Color.BORDER.value}",
        background_color=Color.CONTENT.value,
        align="center",
    )


# ------------------------------------------------------------------ page

def _admin_dashboard() -> rx.Component:
    return rx.vstack(
        _admin_topbar(),
        rx.container(
            rx.vstack(
                rx.heading(
                    "Gestión de productos",
                    size="7",
                    color=TextColor.HEADER.value,
                ),
                rx.text(
                    "Edita el catálogo en vivo. Los cambios se guardan en "
                    "products_config.json y se ven al regenerar el frontend.",
                    color=TextColor.BODY.value,
                ),
                rx.grid(
                    rx.vstack(_section_title("Formulario"), _product_form(), spacing="3", width="100%"),
                    rx.vstack(_products_list(), spacing="3", width="100%"),
                    columns=rx.breakpoints(initial="1", lg="2"),
                    spacing="5",
                    width="100%",
                ),
                # ---- Catálogo PDFs ----
                rx.vstack(
                    _section_title("Catálogos PDF"),
                    rx.text(
                        "Sube archivos PDF para que aparezcan en /catalogo.",
                        color=TextColor.BODY.value, font_size="0.9em",
                    ),
                    rx.hstack(
                        rx.input(
                            placeholder="Nombre del catálogo (ej. Catálogo General 2025)",
                            value=AdminState.pdf_name_input,
                            on_change=AdminState.set_pdf_name_input,
                            width="100%",
                        ),
                        rx.upload(
                            rx.button(rx.icon(tag="upload", size=16), "Subir PDF", size="2"),
                            id="pdf_upload",
                            multiple=True,
                            accept={".pdf": [".pdf"]},
                            on_drop=AdminState.handle_pdf_upload(
                                rx.upload_files(upload_id="pdf_upload")
                            ),
                            width="auto",
                        ),
                        spacing="2",
                        width="100%",
                        align="center",
                    ),
                    rx.cond(
                        AdminState.pdf_upload_feedback != "",
                        rx.callout(AdminState.pdf_upload_feedback, icon="check", color_scheme="green", width="100%"),
                        rx.fragment(),
                    ),
                    rx.cond(
                        AdminState.catalog_pdfs.length() > 0,
                        rx.vstack(
                            rx.foreach(
                                AdminState.catalog_pdfs,
                                lambda pdf: rx.hstack(
                                    rx.icon(tag="file-text", size=16, color=Color.PRIMARY.value),
                                    rx.text(pdf["name"], font_weight="600", color=TextColor.HEADER.value),
                                    rx.text(f"({pdf['file']})", font_size="0.85em", color=TextColor.FOOTER.value),
                                    rx.spacer(),
                                    rx.button(
                                        rx.icon(tag="trash-2", size=14),
                                        size="1", color_scheme="red", variant="soft",
                                        on_click=lambda x=pdf["file"]: AdminState.delete_pdf(x),
                                    ),
                                    width="100%",
                                    padding="0.5em",
                                    align="center",
                                    spacing="3",
                                    border_bottom=f"1px solid {Color.BORDER.value}",
                                ),
                            ),
                            width="100%",
                        ),
                        rx.callout("No hay catálogos PDF subidos.", icon="info", width="100%"),
                    ),
                    rx.cond(
                        AdminState.pdf_delete_feedback != "",
                        rx.callout(AdminState.pdf_delete_feedback, icon="check", color_scheme="green", width="100%"),
                        rx.fragment(),
                    ),
                    spacing="3",
                    width="100%",
                    padding="1.5em",
                    background_color=Color.CONTENT.value,
                    border=f"1px solid {Color.BORDER.value}",
                    border_radius="8px",
                ),
                # ---- Cambiar credenciales ----
                rx.vstack(
                    rx.heading("👤 Cambiar credenciales", size="5", color=TextColor.HEADER.value),
                    rx.text(
                        "Para cambiar usuario o contraseña, introduce tu contraseña anterior "
                        "y recibirás un código SMS de verificación.",
                        color=TextColor.BODY.value,
                        font_size="0.9em",
                    ),
                    # Contraseña anterior (obligatoria para autorizar)
                    rx.input(
                        placeholder="Contraseña anterior",
                        type="password",
                        value=AdminState.old_password_input,
                        on_change=AdminState.set_old_password_input,
                        width="100%",
                    ),
                    # Nuevo usuario (opcional)
                    rx.input(
                        placeholder="Nuevo usuario (dejar vacío si no cambia)",
                        value=AdminState.change_new_username,
                        on_change=AdminState.set_change_new_username,
                        width="100%",
                    ),
                    # Nueva contraseña (opcional)
                    rx.input(
                        placeholder="Nueva contraseña (dejar vacío si no cambia)",
                        type="password",
                        value=AdminState.change_new_password,
                        on_change=AdminState.set_change_new_password,
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Confirmar nueva contraseña",
                        type="password",
                        value=AdminState.change_confirm_password,
                        on_change=AdminState.set_change_confirm_password,
                        width="100%",
                    ),
                    # Teléfono para SMS
                    rx.hstack(
                        rx.text("📱 Teléfono:", font_size="0.9em", color=TextColor.BODY.value, min_width="80px"),
                        rx.input(
                            value=AdminState.change_phone,
                            on_change=AdminState.set_change_phone,
                            width="100%",
                        ),
                        width="100%",
                        align="center",
                    ),
                    rx.cond(
                        AdminState.change_feedback != "",
                        rx.callout(
                            AdminState.change_feedback,
                            icon=rx.cond(
                                AdminState.change_feedback_kind == "success",
                                "check",
                                "alert-triangle",
                            ),
                            color_scheme=rx.cond(
                                AdminState.change_feedback_kind == "success",
                                "green",
                                "red",
                            ),
                            width="100%",
                        ),
                    ),
                    # Botón enviar código SMS
                    rx.cond(
                        AdminState.sms_step == "input",
                        rx.button(
                            "Enviar código SMS",
                            on_click=AdminState.send_sms_code,
                            size="3",
                            width="100%",
                        ),
                    ),
                    # Verificación SMS
                    rx.cond(
                        AdminState.sms_step == "code_sent",
                        rx.vstack(
                            rx.input(
                                placeholder="Código de verificación",
                                value=AdminState.sms_code_input,
                                on_change=AdminState.set_sms_code_input,
                                width="100%",
                            ),
                            rx.button(
                                "Verificar y guardar",
                                on_click=AdminState.verify_sms_and_save,
                                size="3",
                                width="100%",
                            ),
                            spacing="2",
                            width="100%",
                        ),
                    ),
                    spacing="3",
                    width="100%",
                    padding="1.5em",
                    background_color=Color.CONTENT.value,
                    border=f"1px solid {Color.BORDER.value}",
                    border_radius="8px",
                ),
                spacing="5",
                width="100%",
                padding_y="2em",
            ),
            max_width=styles.MAX_WIDTH,
            padding_x="1em",
        ),
        width="100%",
        min_height="100vh",
        background_color=Color.BACKGROUND.value,
        spacing="0",
        on_mount=AdminState.on_load,
    )


def admin_page() -> rx.Component:
    """Página /admin: muestra login o dashboard según estado."""
    return rx.cond(
        AdminState.is_admin_authenticated,
        _admin_dashboard(),
        _login_screen(),
    )