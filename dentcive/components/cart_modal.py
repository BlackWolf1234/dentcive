import reflex as rx
from dentcive.styles.colors import Color, TextColor
from dentcive.styles.styles import Size
from dentcive.state import State


def cart_item_row(item: dict) -> rx.Component:
    """Fila de un ítem del carrito con nombre, precio, cantidad y botón de eliminar."""
    return rx.hstack(
        rx.text(item.get("product_id", ""), font_size="0.9em", color=TextColor.BODY.value),
        rx.spacer(),
        rx.text(item.get("price", 0), font_weight="bold", color=Color.PRIMARY.value),
        rx.text("x" + item.get("qty", 0).to_string(), color=TextColor.FOOTER.value),
        rx.button(
            "🗑",
            size="1",
            background_color="transparent",
            color=Color.SALE.value,
            # Elimina el producto del carrito al hacer clic
            on_click=State.remove_from_cart(item["product_id"]),
        ),
        width="100%",
        padding="0.5em",
        border_bottom=f"1px solid {Color.BORDER.value}",
        align="center",
    )


def cart_summary() -> rx.Component:
    """Resumen del carrito con subtotal, descuento y total calculados desde el estado."""
    return rx.vstack(
        rx.hstack(
            rx.text("Subtotal:", font_weight="bold"),
            rx.spacer(),
            # Usa la computed var del estado (calcula precio × cantidad de cada ítem)
            rx.text(State.cart_subtotal_str, color=TextColor.BODY.value),
            width="100%",
        ),
        # Fila de descuento: sólo visible si hay cupón activo
        rx.cond(
            State.coupon_discount > 0,
            rx.hstack(
                rx.text("Descuento:", font_weight="bold", color=Color.PRIMARY.value),
                rx.spacer(),
                rx.text(State.cart_discount_str, color=Color.PRIMARY.value),
                width="100%",
            ),
            rx.fragment(),
        ),
        rx.divider(),
        rx.hstack(
            rx.text("Total:", size="5", font_weight="bold", color=Color.PRIMARY.value),
            rx.spacer(),
            rx.text(State.cart_total_str, size="5", font_weight="bold", color=Color.PRIMARY.value),
            width="100%",
        ),
        spacing="2",
        width="100%",
    )


def cart_modal() -> rx.Component:
    """Modal del carrito de compras (overlay fijo centrado en pantalla)."""
    return rx.cond(
        State.show_cart_modal,
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.heading("Tu Carrito", size="5"),
                    rx.spacer(),
                    rx.button(
                        "✕",
                        on_click=State.toggle_cart_modal,
                        background_color="transparent",
                        border="none",
                        font_size="1.5em",
                    ),
                    width="100%",
                    align="center",
                ),
                rx.cond(
                    State.cart_items.length() > 0,
                    rx.vstack(
                        rx.foreach(State.cart_items, lambda item: cart_item_row(item)),
                        # Input de cupón controlado + botón de aplicar
                        rx.hstack(
                            rx.input(
                                placeholder="Código de cupón",
                                value=State.coupon_input,
                                on_change=State.set_coupon_input,
                                width="100%",
                            ),
                            rx.button(
                                "Aplicar cupón",
                                size="1",
                                on_click=State.apply_coupon,
                            ),
                            width="100%",
                            spacing="2",
                        ),
                        cart_summary(),
                        rx.button(
                            "Proceder al pago",
                            width="100%",
                            background_color=Color.PRIMARY.value,
                            size="3",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    # Carrito vacío
                    rx.vstack(
                        rx.text(
                            "Tu carrito está vacío",
                            text_align="center",
                            color=TextColor.BODY.value,
                        ),
                        rx.button(
                            "Continuar comprando",
                            width="100%",
                            on_click=State.toggle_cart_modal,
                        ),
                        spacing="2",
                        width="100%",
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
