"""Página /servicio-tecnico."""
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


def service_hero() -> rx.Component:
    """Cabecera de la página de Servicio Técnico."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "Servicio Técnico",
                size="8",
                color="#ffffff",
                text_align="center",
            ),
            rx.text(
                "Reparación de instrumental rotatorio, mantenimiento y asistencia "
                "especializada para clínicas y laboratorios dentales.",
                size="4",
                color="#ffffff",
                text_align="center",
                max_width="720px",
            ),
            rx.hstack(
                rx.link(
                    rx.button(
                        rx.icon(tag="wrench", size=20),
                        "Solicitar presupuesto",
                        size="3",
                        background_color=Color.ACCENT.value,
                        color="#111111",
                        _hover={"background_color": "#ffd84d"},
                    ),
                    href="mailto:dentcive@gmail.com?subject=Solicitud%20de%20servicio%20t%C3%A9cnico",
                ),
                rx.link(
                    rx.button(
                        rx.icon(tag="phone", size=20),
                        "Llamar",
                        size="3",
                        variant="soft",
                    ),
                    href="tel:+34943369790",
                ),
                spacing="3",
                wrap="wrap",
                justify="center",
            ),
            spacing="4",
            align="center",
            padding="3em 1em",
            background="rgba(0, 0, 0, 0.55)",
            width="100%",
        ),
        background_image="url('/dentcive-clinic-bg.jpg')",
        background_size="cover",
        background_position="center",
        width="100%",
    )


def service_card(title: str, body: str, icon: str, bg: str, wa_msg: str = "") -> rx.Component:
    whatsapp_url = f"https://wa.me/34661921722?text={wa_msg}"
    return rx.vstack(
        rx.icon(tag=icon, size=34, color="#ffffff"),
        rx.heading(title, size="4", color="#ffffff", text_align="center", line_height="1.05"),
        rx.text(body, color="#ffffff", text_align="center", font_size="0.9em"),
        rx.spacer(),
        rx.link(
            rx.button(rx.icon(tag="message-circle", size=17), "Consultar", size="2"),
            href=whatsapp_url,
            is_external=True,
        ),
        background_color=bg,
        padding="1.4em",
        min_height="260px",
        justify="center",
        align="center",
        spacing="3",
    )


def service_page() -> rx.Component:
    """Página completa /servicio-tecnico."""
    return rx.box(
        navbar(is_home=False),
        rx.center(
            rx.vstack(
                service_hero(),
                rx.grid(
                    service_card(
                        "Mantenimiento preventivo",
                        "Revisión periódica para asegurar el óptimo funcionamiento de tu equipamiento dental.",
                        "heart-pulse",
                        "#1e3a5f",
                        "Hola%2C%20quiero%20informacion%20sobre%20Mantenimiento%20preventivo",
                    ),
                    service_card(
                        "Mantenimiento correctivo",
                        "Diagnóstico y reparación de averías para recuperar la operatividad de tus equipos.",
                        "wrench",
                        "#2b5a9a",
                        "Hola%2C%20quiero%20informacion%20sobre%20Mantenimiento%20correctivo",
                    ),
                    service_card(
                        "Reparación instrumental rotatorio",
                        "Reparación profesional de turbinas, contra-ángulos, piezas de mano y micromotores.",
                        "rotate-cw",
                        "#3b7dd8",
                        "Hola%2C%20quiero%20informacion%20sobre%20Reparaci%C3%B3n%20instrumental%20rotatorio",
                    ),
                    service_card(
                        "Asesoramiento",
                        "Consultoría personalizada para reforma, creación de clínicas y gestión de equipamiento.",
                        "messages-square",
                        "#5a9bf5",
                        "Hola%2C%20quiero%20informacion%20sobre%20Asesoramiento",
                    ),
                    columns=rx.breakpoints(initial="1", sm="2", md="4"),
                    spacing="0",
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
        on_mount=State.reload_products,
        padding_top=rx.breakpoints(initial="120px", md="155px"),
        overflow_x="hidden",
    )