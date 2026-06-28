import reflex as rx

from dentcive.components.auth_modal import auth_modal
from dentcive.components.cart_modal import cart_modal
from dentcive.components.wishlist_sidebar import wishlist_modal
from dentcive.components.footer import footer
from dentcive.components.navbar import navbar
from dentcive.components.product_card import product_card
from dentcive.data.products import CATEGORIES, SUBCATEGORIES
from dentcive.state import State
from dentcive.styles.colors import Color, TextColor
from dentcive.styles.styles import Size
import dentcive.styles.styles as styles


def _filter_btn(label: str, icon: str, cat: str, active) -> rx.Component:
    return rx.button(
        rx.hstack(
            rx.icon(tag=icon, size=16),
            rx.text(label, font_size="0.85em"),
            spacing="1",
        ),
        size="2",
        variant=rx.cond(active, "solid", "soft"),
        background_color=rx.cond(active, Color.FILTER_ACTIVE.value, ""),
        on_click=State.set_store_filter_category(cat),
        width="100%",
    )


def _rotatorio_filter_btn() -> rx.Component:
    return rx.menu.root(
        rx.menu.trigger(
            rx.button(
                rx.hstack(
                    rx.icon(tag="rotate-cw", size=16),
                    rx.text("Rotatorio", font_size="0.85em"),
                    spacing="1",
                ),
                size="2",
                variant=rx.cond(State.store_filter_category == "rotatorio", "solid", "soft"),
                background_color=rx.cond(State.store_filter_category == "rotatorio", Color.FILTER_ACTIVE.value, ""),
                width="100%",
            ),
        ),
        rx.menu.content(
            rx.menu.item("Todas las categorías", on_click=State.set_store_filter_category("rotatorio")),
            rx.menu.separator(),
            rx.menu.item("Turbina", on_click=State.set_store_filter_subcategory("turbina")),
            rx.menu.item("Contra-Ángulos", on_click=State.set_store_filter_subcategory("contra-angulos")),
            rx.menu.item("Pieza de Mano", on_click=State.set_store_filter_subcategory("pieza-mano")),
            rx.menu.item("Jeringa Agua/Aire", on_click=State.set_store_filter_subcategory("jeringa")),
            rx.menu.item("Micromotores", on_click=State.set_store_filter_subcategory("micromotores")),
        ),
    )


def store_filter() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon(tag="filter", size=18, color=Color.PRIMARY.value),
            rx.text("Filtrar por categoría", font_weight="700", color=TextColor.HEADER.value),
            rx.spacer(),
            rx.cond(
                State.store_filter_category != "",
                rx.button(
                    "Limpiar filtro",
                    size="1",
                    variant="soft",
                    on_click=State.clear_store_filter,
                ),
            ),
            width="100%",
            align="center",
        ),
        rx.grid(
            _filter_btn("Ofertas", "badge-euro", "ofertas", State.store_filter_category == "ofertas"),
            _filter_btn("Equipos", "monitor-cog", "equipos", State.store_filter_category == "equipos"),
            _filter_btn("Compresores", "wind", "compresores", State.store_filter_category == "compresores"),
            _filter_btn("Aspiraciones", "air-vent", "aspiraciones", State.store_filter_category == "aspiraciones"),
            _filter_btn("Autoclaves", "thermometer", "autoclaves", State.store_filter_category == "autoclaves"),
            _filter_btn("Selladoras", "container", "selladoras", State.store_filter_category == "selladoras"),
            _filter_btn("Ultrasonidos", "radio", "ultrasonidos", State.store_filter_category == "ultrasonidos"),
            _rotatorio_filter_btn(),
            columns=rx.breakpoints(initial="2", sm="3", md="4"),
            spacing="2",
            width="100%",
        ),
        spacing="3",
        width="100%",
        padding="1em",
        background_color=Color.CONTENT.value,
        border=f"1px solid {Color.BORDER.value}",
        border_radius="8px",
    )


def store_hero() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Tienda Dentcive", size="8", color="#ffffff", text_align="center"),
            rx.text(
                "Todos nuestros productos dentales, equipamiento y servicio técnico.",
                size="4", color="#ffffff", text_align="center", max_width="720px",
            ),
            spacing="3", align="center", padding="3em 1em",
            background="rgba(0, 0, 0, 0.55)", width="100%",
        ),
        background_image="url('/dentcive-clinic-bg.jpg')",
        background_size="cover", background_position="center", width="100%",
    )


def store_page() -> rx.Component:
    return rx.box(
        navbar(is_home=False),
        rx.center(
            rx.vstack(
                store_hero(),
                store_filter(),
                rx.grid(
                    rx.foreach(State.filtered_store_products, lambda p: product_card(p)),
                    columns=rx.breakpoints(initial="1", sm="2", md="3", lg="4"),
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
        on_mount=State.load_store_page,
        padding_top=rx.breakpoints(initial="120px", md="155px"),
        overflow_x="hidden",
    )
