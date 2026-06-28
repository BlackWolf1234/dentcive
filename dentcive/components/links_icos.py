import reflex as rx


def links_icon(url: str, tag: str) -> rx.Component:
    return rx.link(
        rx.icon(
            tag=tag,
            size=40,
            color="cyan",
        ),
        href=url,
        is_external=True,
    )
