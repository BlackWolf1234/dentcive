import reflex as rx
import dentcive.styles.styles as styles
from dentcive.styles.colors import TextColor as TextColor
from dentcive.styles.styles import Size as Size


def links_button(text: str, url: str, tag: str) -> rx.Component:
    return rx.link(
        rx.button(
            rx.hstack(
                rx.icon(
                    tag=tag,
                    width=Size.BIG.value,
                    height=Size.BIG.value,
                    margin=Size.MEDIUM.value,
                    color=TextColor.FOOTER.value,
                ),
                rx.text(text, style=styles.button_title_style),
                align_items="start",
                margin=Size.Zero.value,
                width="100%",
            ),
        ),
        href=url,
        is_external=True,
    )
