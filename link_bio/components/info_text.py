import reflex as rx
from link_bio.styles.styles import Size as Size
from link_bio.styles.colors import TextColor as TextColor
from link_bio.styles.colors import Color as Color


def info_text(title: str, body: str) -> rx.Component:
    return rx.box(
        rx.text.span(
            title,
            font_weight="bold",
            color=Color.PRIMARY.value,
        ),
        body,
        font_size=Size.MEDIUM.value,
        color=TextColor.BODY.value,
    )
