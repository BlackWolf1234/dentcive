import reflex as rx
from dentcive.styles.colors import Color, TextColor
from dentcive.state import State


def wishlist_modal() -> rx.Component:
    return rx.cond(
        State.show_wishlist_modal,
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.heading(State.translations["wishlist_title"], size="5"),
                    rx.spacer(),
                    rx.button(
                        "✕",
                        on_click=State.toggle_wishlist_modal,
                        background_color="transparent",
                        border="none",
                        font_size="1.5em",
                    ),
                    width="100%",
                    align="center",
                ),
                rx.cond(
                    State.wishlist_ids.length() > 0,
                    rx.vstack(
                        rx.foreach(
                            State.wishlist_ids,
                            lambda pid: rx.hstack(
                                rx.text(pid, font_size="0.9em", color=TextColor.BODY.value),
                                rx.spacer(),
                                rx.button(
                                    "✕",
                                    size="1",
                                    background_color="transparent",
                                    color=Color.SALE.value,
                                    on_click=State.toggle_wishlist(pid),
                                ),
                                width="100%",
                                padding="0.5em",
                                border_bottom=f"1px solid {Color.BORDER.value}",
                            ),
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    rx.text(
                        State.translations["empty_wishlist"],
                        text_align="center",
                        color=TextColor.BODY.value,
                    ),
                ),
                spacing="4",
                padding="2em",
                background_color=Color.CONTENT.value,
                border_radius="8px",
                width="100%",
                max_width="500px",
                max_height="80vh",
                overflow_y="auto",
            ),
            position="fixed",
            top="50%",
            left="50%",
            transform="translate(-50%, -50%)",
            z_index="1000",
            background_color="rgba(0, 0, 0, 0.5)",
            width="100vw",
            height="100vh",
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        rx.fragment(),
    )
