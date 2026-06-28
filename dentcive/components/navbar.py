import reflex as rx
from dentcive.styles.styles import Size as Size
import dentcive.styles.styles as style
from dentcive.styles.colors import Color as Color
from dentcive.styles.colors import TextColor as TextColor
from dentcive.data.products import CATEGORIES, SUBCATEGORIES
from dentcive.state import State


def _anchor(hash_href: str, is_home: bool) -> str:
    return hash_href if is_home else "/" + hash_href


def nav_link(text: str, href: str) -> rx.Component:
    return rx.link(
        text,
        href=href,
        color=Color.DARK.value,
        font_weight="600",
        font_size="0.95em",
        _hover={"color": Color.PRIMARY.value},
    )


def navbar(is_home: bool = True) -> rx.Component:
    """Navbar global. Recibe ``is_home`` para construir anchors correctos."""
    return rx.vstack(
        rx.hstack(
            rx.hstack(
                rx.icon(tag="phone", size=16, color=Color.PRIMARY.value),
                rx.text("+34 943 369 790", color=TextColor.BODY.value, font_size="0.85em"),
                rx.text("+34 661 921 722", color=TextColor.BODY.value, font_size="0.85em"),
                rx.icon(tag="mail", size=16, color=Color.PRIMARY.value),
                rx.text("dentcive@gmail.com", color=TextColor.BODY.value, font_size="0.85em"),
                spacing="3",
                wrap="wrap",
                display=rx.breakpoints(initial="none", md="flex"),
            ),
            rx.spacer(),
            rx.hstack(
                rx.link(State.translations["home"], href=_anchor("#inicio", is_home), color=TextColor.BODY.value),
                rx.link(State.translations["contact_us"], href=_anchor("#contacto", is_home), color=TextColor.BODY.value),
                spacing="4",
                display=rx.breakpoints(initial="none", md="flex"),
            ),
            width="100%",
            max_width=style.MAX_WIDTH,
            padding_x=Size.DEFAULT.value,
            padding_y="0.5em",
            align="center",
        ),
        rx.hstack(
            rx.link(
                rx.image(src="/dentcive-logo-retina.png", alt="Dentcive", width=rx.breakpoints(initial="140px", md="180px"), height="auto"),
                href=_anchor("#inicio", is_home),
                min_width=rx.breakpoints(initial="140px", md="180px"),
            ),
            rx.hstack(
                rx.icon(tag="search", size=18, color=Color.DARK.value, cursor="pointer", on_click=State.do_search),
                rx.input(
                    placeholder="Buscar productos, marcas o referencias",
                    value=State.search_query,
                    on_change=State.set_search_query,
                    width="100%",
                    background_color="transparent",
                    border="none",
                    outline="none",
                    box_shadow="none",
                    font_size="0.9em",
                    color=Color.DARK.value,
                    _placeholder={"color": "#94a3b8"},
                    _focus={"border": "none", "outline": "none", "box_shadow": "none", "ring": "none"},
                ),
                background_color=Color.SURFACE.value,
                border_radius="9999px",
                padding="0.55em 1.2em",
                width="100%",
                display=rx.breakpoints(initial="none", md="flex"),
                align="center",
                spacing="2",
            ),
            rx.spacer(),
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon(tag="heart", size=22),
                        rx.cond(
                            State.wishlist_ids.length() > 0,
                            rx.badge(State.wishlist_ids.length(), color_scheme="red"),
                            rx.fragment(),
                        ),
                        spacing="1",
                    ),
                    background_color="transparent",
                    border="none",
                    color=Color.DARK.value,
                    on_click=State.toggle_wishlist_modal,
                ),
                rx.button(
                    rx.hstack(
                        rx.icon(tag="user", size=22),
                        rx.cond(
                            State.is_logged_in,
                            rx.text(State.username, font_size="0.9em"),
                            rx.text(State.translations["account"], font_size="0.9em"),
                        ),
                        spacing="1",
                    ),
                    background_color="transparent",
                    border="none",
                    color=Color.DARK.value,
                    on_click=State.toggle_login_modal,
                ),
                rx.button(
                    rx.hstack(
                        rx.icon(tag="shopping-cart", size=22),
                        rx.text("Carrito", font_weight="700"),
                        rx.cond(
                            State.cart_items.length() > 0,
                            rx.badge(State.cart_items.length(), color_scheme="blue"),
                            rx.fragment(),
                        ),
                        spacing="2",
                    ),
                    background_color="transparent",
                    border="none",
                    color=Color.DARK.value,
                    on_click=State.toggle_cart_modal,
                ),
                spacing="4",
            ),
            width="100%",
            max_width=style.MAX_WIDTH,
            padding_x=Size.DEFAULT.value,
            padding_y=Size.DEFAULT.value,
            align="center",
        ),
        rx.hstack(
            rx.menu.root(
                rx.menu.trigger(
                    rx.button(
                        State.translations["store"],
                        color=Color.DARK.value,
                        font_weight="600",
                        font_size="0.95em",
                        background_color="transparent",
                        border="none",
                        _hover={"color": Color.PRIMARY.value},
                    ),
                ),
                rx.menu.content(
                    rx.menu.item(
                        rx.hstack(
                            rx.icon(tag="shopping-bag", size=16),
                            rx.text("Todos los productos"),
                            spacing="2",
                        ),
                        on_click=rx.redirect("/tienda"),
                    ),
                    rx.menu.separator(),
                    rx.menu.item(
                        rx.hstack(rx.icon(tag="badge-euro", size=16), rx.text("Ofertas"), spacing="2"),
                        on_click=rx.redirect("/tienda?cat=ofertas"),
                    ),
                    rx.menu.item(
                        rx.hstack(rx.icon(tag="monitor-cog", size=16), rx.text("Equipos"), spacing="2"),
                        on_click=rx.redirect("/tienda?cat=equipos"),
                    ),
                    rx.menu.item(
                        rx.hstack(rx.icon(tag="wind", size=16), rx.text("Compresores"), spacing="2"),
                        on_click=rx.redirect("/tienda?cat=compresores"),
                    ),
                    rx.menu.item(
                        rx.hstack(rx.icon(tag="air-vent", size=16), rx.text("Aspiraciones"), spacing="2"),
                        on_click=rx.redirect("/tienda?cat=aspiraciones"),
                    ),
                    rx.menu.item(
                        rx.hstack(rx.icon(tag="thermometer", size=16), rx.text("Autoclaves"), spacing="2"),
                        on_click=rx.redirect("/tienda?cat=autoclaves"),
                    ),
                    rx.menu.item(
                        rx.hstack(rx.icon(tag="container", size=16), rx.text("Selladoras"), spacing="2"),
                        on_click=rx.redirect("/tienda?cat=selladoras"),
                    ),
                    rx.menu.item(
                        rx.hstack(rx.icon(tag="radio", size=16), rx.text("Ultrasonidos"), spacing="2"),
                        on_click=rx.redirect("/tienda?cat=ultrasonidos"),
                    ),
                    rx.menu.sub(
                        rx.menu.sub_trigger(
                            rx.hstack(rx.icon(tag="rotate-cw", size=16), rx.text("Rotatorio"), spacing="2"),
                        ),
                        rx.menu.sub_content(
                            rx.menu.item("Turbina", on_click=rx.redirect("/tienda?cat=rotatorio&sub=turbina")),
                            rx.menu.item("Contra-Ángulos", on_click=rx.redirect("/tienda?cat=rotatorio&sub=contra-angulos")),
                            rx.menu.item("Pieza de Mano", on_click=rx.redirect("/tienda?cat=rotatorio&sub=pieza-mano")),
                            rx.menu.item("Jeringa Agua/Aire", on_click=rx.redirect("/tienda?cat=rotatorio&sub=jeringa")),
                            rx.menu.item("Micromotores", on_click=rx.redirect("/tienda?cat=rotatorio&sub=micromotores")),
                        ),
                    ),
                ),
            ),
            nav_link(State.translations["technical_service"], "/servicio-tecnico"),
            nav_link(State.translations["brands"], _anchor("#marcas", is_home)),
            nav_link(State.translations["catalog"], "/catalogo"),
            nav_link(State.translations["contact_us"], _anchor("#contacto", is_home)),
            nav_link(State.translations["about_us"], _anchor("#nosotros", is_home)),
            spacing="6",
            overflow_x="auto",
            width="100%",
            max_width=style.MAX_WIDTH,
            padding_x=Size.DEFAULT.value,
            padding_y="0.75em",
        ),
        align="center",
        width="100%",
        position="fixed",
        bg=Color.CONTENT.value,
        border_bottom=f"1px solid {Color.BORDER.value}",
        z_index="999",
        top="0",
        spacing="0",
    )
