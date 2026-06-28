import reflex as rx
from dentcive.styles.colors import Color, TextColor
from dentcive.styles.styles import Size


def newsletter_section() -> rx.Component:
    """Newsletter subscription section."""
    return rx.vstack(
        rx.heading("Suscríbete a Nuestro Newsletter", size="5", color="white", text_align="center"),
        rx.text(
            "Recibe ofertas exclusivas y novedades de Dentcive directamente en tu email.",
            text_align="center",
            color="white",
            font_size="0.95em",
        ),
        rx.hstack(
            rx.input(
                placeholder="tu@email.com",
                type_="email",
                width="100%",
            ),
            rx.button(
                "Suscribirse",
                background_color="white",
                color=Color.PRIMARY.value,
                font_weight="bold",
            ),
            width="100%",
            spacing="2",
        ),
        rx.text(
            "✓ Sin spam, solo contenido de valor",
            font_size="0.8em",
            color="rgba(255,255,255,0.7)",
            text_align="center",
        ),
        spacing="3",
        padding="2em",
        background_color=Color.PRIMARY.value,
        border_radius="8px",
        width="100%",
        align_items="center",
    )
