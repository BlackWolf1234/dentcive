"""Página /catalogo: muestra PDFs del catálogo."""
import reflex as rx

from dentcive.components.auth_modal import auth_modal
from dentcive.components.cart_modal import cart_modal
from dentcive.components.wishlist_sidebar import wishlist_modal
from dentcive.components.footer import footer
from dentcive.components.navbar import navbar
from dentcive.styles.colors import Color, TextColor
from dentcive.styles.styles import Size
from dentcive.state import State
import dentcive.styles.styles as styles


def catalog_hero() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Catálogo Dentcive", size="8", color="#ffffff", text_align="center"),
            rx.text(
                "Descarga nuestros catálogos en PDF.",
                size="4", color="#ffffff", text_align="center", max_width="720px",
            ),
            spacing="3", align="center", padding="3em 1em",
            background="rgba(0, 0, 0, 0.55)", width="100%",
        ),
        background_image="url('/dentcive-clinic-bg.jpg')",
        background_size="cover", background_position="center", width="100%",
    )


def _pdf_card(pdf: dict) -> rx.Component:
    return rx.link(
        rx.vstack(
            rx.icon(tag="file-text", size=48, color=Color.PRIMARY.value),
            rx.heading(pdf["name"], size="4", color=TextColor.HEADER.value, text_align="center"),
            background_color=Color.CONTENT.value,
            border=f"1px solid {Color.BORDER.value}",
            border_radius="8px",
            padding="2em",
            min_height="180px",
            justify="center",
            align="center",
            spacing="3",
            _hover={"border_color": Color.PRIMARY.value, "box_shadow": "0 4px 12px rgba(0,0,0,0.1)"},
        ),
        href=pdf["url"],
        is_external=True,
    )


def catalog_page() -> rx.Component:
    return rx.box(
        navbar(is_home=False),
        rx.center(
            rx.vstack(
                catalog_hero(),
                rx.grid(
                    rx.foreach(State.catalog_pdfs, _pdf_card),
                    columns=rx.breakpoints(initial="1", sm="2", md="3"),
                    spacing="4",
                    width="100%",
                    padding_y=Size.BIG.value,
                ),
                footer(),
                max_width=styles.MAX_WIDTH,
                width="100%",
                padding_x=Size.DEFAULT.value,
                align="center",
            ),
            width="100%",
        ),
        auth_modal(),
        cart_modal(),
        wishlist_modal(),
        on_mount=State.load_catalog_page,
        padding_top=rx.breakpoints(initial="120px", md="155px"),
        overflow_x="hidden",
    )