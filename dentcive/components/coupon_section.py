import reflex as rx
from dentcive.styles.colors import Color, TextColor
from dentcive.data.products import COUPONS
from dentcive.state import State


def coupon_card(code: str, discount: int, description: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(code, font_weight="bold", size="4", color=Color.PRIMARY.value),
                rx.spacer(),
                rx.text(f"{discount}% OFF", font_weight="bold", color=Color.SALE.value),
                width="100%",
            ),
            rx.text(description, font_size="0.9em", color=TextColor.BODY.value),
            rx.button(
                State.translations["apply"],
                width="100%",
                size="2",
                background_color=Color.SECONDARY.value,
                on_click=State.apply_coupon_code(code),
            ),
            spacing="2",
            width="100%",
        ),
        padding="1em",
        border=f"2px solid {Color.BORDER.value}",
        border_radius="8px",
        background_color=Color.SURFACE.value,
    )


def coupon_section() -> rx.Component:
    return rx.vstack(
        rx.heading(State.translations["coupons_title"], size="5", color=TextColor.HEADER.value),
        rx.grid(
            rx.foreach(
                COUPONS,
                lambda c: coupon_card(c["code"], c["discount"], c["description_es"]),
            ),
            columns=rx.breakpoints(initial="1", md="3"),
            spacing="3",
            width="100%",
        ),
        spacing="3",
        padding="2em",
        background_color=Color.BACKGROUND.value,
        border_radius="8px",
        width="100%",
    )
