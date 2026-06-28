import reflex as rx
import datetime
from dentcive.styles.styles import Size as Size
from dentcive.styles.colors import TextColor as TextColor
from dentcive.styles.colors import Color as Color


def footer_link(text: str, href: str = "#") -> rx.Component:
    return rx.link(text, href=href, color="#d9e6ee")


def footer_column(title: str, *items) -> rx.Component:
    return rx.vstack(
        rx.text(title, color="#ffffff", font_weight="900"),
        *[footer_link(text, href) for text, href in items],
        align_items="start",
        spacing="2",
    )


def footer() -> rx.Component:
    return rx.vstack(
        rx.grid(
            rx.vstack(
                rx.image(src="/logo-dentcive-dark.png", alt="Dentcive", width=rx.breakpoints(initial="150px", md="190px"), height="auto"),
                rx.text(
                    "Empresa dedicada a la distribución de productos dentales, reparación de instrumental rotatorio y servicio técnico para clínicas.",
                    color="#d9e6ee",
                ),
               
                align_items="start",
                spacing="3",
            ),
            footer_column(
                "Información",
                ("Inicio", "#inicio"),
                ("Servicios", "#servicios"),
                ("Nosotros", "#nosotros"),
                ("Catálogo", "#productos"),
            ),
            footer_column(
                "Contacto",
                ("Zirkuito Ibilbidea, 10", "#contacto"),
                ("20160 Lasarte-Oria, Gipuzkoa", "#contacto"),
                ("+34 943 369 790", "tel:+34943369790"),
                ("dentcive@gmail.com", "mailto:dentcive@gmail.com"),
            ),
            footer_column(
                "Servicios",
                ("Área comercial", "#servicios"),
                ("Reparación rotatorio", "#servicios"),
                ("Servicio técnico", "#servicios"),
                ("Asesoramiento personalizado", "#servicios"),
            ),
            columns=rx.breakpoints(initial="1", md="4"),
            spacing="6",
            width="100%",
        ),
        rx.hstack(
            rx.text(
                f"Copyright {datetime.date.today().year} Dentcive.",
                font_size=Size.MEDIUM.value,
                color="#d9e6ee",
            ),
            rx.spacer(),
            rx.hstack(
                footer_link("Newsletter", "mailto:dentcive@gmail.com?subject=Newsletter"),
                footer_link("Contacto", "#contacto"),
                spacing="4",
            ),
            width="100%",
            align="center",
            wrap="wrap",
            border_top="1px solid rgba(255, 255, 255, 0.18)",
            padding_top=Size.DEFAULT.value,
        ),
        width="100%",
        margin_bottom=Size.BIG.value,
        padding=Size.BIG.value,
        background_color="#191919",
        color=TextColor.FOOTER.value,
        spacing="6",
    )
