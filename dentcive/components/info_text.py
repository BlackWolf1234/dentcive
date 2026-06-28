import reflex as rx
from dentcive.styles.styles import Size as Size
from dentcive.styles.colors import TextColor as TextColor
from dentcive.styles.colors import Color as Color


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
        background_color=Color.CONTENT.value,
        border=f"1px solid {Color.BORDER.value}",
        border_radius="8px",
        padding="0.75em 1em",
    )
