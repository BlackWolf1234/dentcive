import reflex as rx
from dentcive.styles.colors import Color as Color
from dentcive.styles.colors import TextColor as TextColor
from dentcive.state import State


def _budget_button(product: dict) -> rx.Component:
    return rx.cond(
        product["price"] > 0,
        rx.link(
            rx.button(rx.icon(tag="message-circle", size=17), "Consultar", size="2"),
            href=product["wa_url"],
            is_external=True,
        ),
        rx.link(
            rx.button(rx.icon(tag="file-text", size=17), "Solicitar Presupuesto"),
            href=product["budget_url"],
        ),
    )


def product_card(product: dict) -> rx.Component:
    pid = product["id"]
    name = product["name"]["es"]
    description = product["description"]["es"]
    category_label = product["category"]

    return rx.box(
        rx.box(
            rx.button(
                rx.cond(
                    State.wishlist_ids.contains(pid),
                    rx.icon(tag="heart", size=18, color="#ef4444", fill="#ef4444"),
                    rx.icon(tag="heart", size=18, color="#ffffff"),
                ),
                position="absolute",
                top="0.5em",
                right="0.5em",
                z_index="2",
                background_color="rgba(0,0,0,0.35)",
                border_radius="50%",
                width="36px",
                height="36px",
                padding="0",
                display="flex",
                align_items="center",
                justify_content="center",
                transition="all 0.2s",
                _hover={"background_color": "rgba(0,0,0,0.6)", "transform": "scale(1.1)"},
                on_click=State.toggle_wishlist(pid),
            ),
            rx.image(
                src="/" + product["image"],
                width="100%",
                height="170px",
                object_fit="cover",
            ),
            position="relative",
            background_color=Color.MUTED.value,
        ),
        rx.vstack(
            rx.hstack(
                rx.text(category_label, color=Color.PRIMARY.value, font_weight="700", font_size="0.78em"),
                rx.cond(
                    product["brand_or_empty"] != "",
                    rx.text("· " + product["brand_or_empty"], color=TextColor.FOOTER.value, font_size="0.78em"),
                ),
                rx.spacer(),
                rx.cond(
                    product["tag_or_empty"] != "",
                    rx.badge(product["tag_or_empty"], color_scheme="blue", variant="soft", font_size="0.7em"),
                ),
                width="100%",
                align="center",
            ),
            rx.heading(name, size="3", color=TextColor.HEADER.value, min_height="54px"),
            rx.text(description, color=TextColor.BODY.value, font_size="0.88em", min_height="44px"),
            rx.hstack(
                rx.cond(
                    product["price"] > 0,
                    rx.vstack(
                        rx.text(product["price_str"], font_weight="bold", size="5", color=Color.PRIMARY.value),
                        rx.cond(
                            product["old_price_str"] != "",
                            rx.text(product["old_price_str"], as_="s", color=TextColor.FOOTER.value, font_size="0.85em"),
                        ),
                        align_items="start",
                        spacing="0",
                    ),
                    rx.text("Sin precio", font_weight="bold", size="2", color=TextColor.FOOTER.value),
                ),
                rx.spacer(),
                _budget_button(product),
                width="100%",
                align="center",
            ),
            align_items="start",
            spacing="2",
            padding="1em",
        ),
        background_color=Color.CONTENT.value,
        border=f"1px solid {Color.BORDER.value}",
        border_radius="4px",
        overflow="hidden",
        height="100%",
    )