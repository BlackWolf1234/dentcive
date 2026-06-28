import reflex as rx
import dentcive.styles.styles as styles


def title(text: str) -> rx.Component:
    return rx.heading(
        text,
        style=styles.titulo_style,
    )
