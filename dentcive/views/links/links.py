import reflex as rx
from dentcive.components.titulos import title
from dentcive.components.product_card import product_card
from dentcive.data.products import CATEGORIES
from dentcive.styles.colors import Color as Color
from dentcive.styles.colors import TextColor as TextColor
from dentcive.styles.styles import Size as Size
from dentcive.state import State


def section_header(text: str, action: str, href: str) -> rx.Component:
    return rx.hstack(
        title(text),
        rx.spacer(),
        rx.link(action, href=href, color=Color.PRIMARY.value, font_weight="700"),
        width="100%",
        align="center",
    )


def category_card(name: str, icon: str) -> rx.Component:
    return rx.link(
        rx.vstack(
            rx.icon(tag=icon, size=34, color=Color.PRIMARY.value),
            rx.text(name, color=TextColor.HEADER.value, font_weight="800", text_align="center"),
            background_color=Color.CONTENT.value,
            border=f"1px solid {Color.BORDER.value}",
            border_radius="4px",
            padding="1.25em",
            min_height="128px",
            justify="center",
            spacing="3",
        ),
        href="#productos",
    )


def trust_card(title_text: str, body: str, icon: str, bg: str) -> rx.Component:
    return rx.vstack(
        rx.icon(tag=icon, size=30, color="#ffffff"),
        rx.heading(title_text, size="4", color="#ffffff", text_align="center"),
        rx.text(body, color="#ffffff", text_align="center", font_size="0.92em"),
        background_color=bg,
        padding="1.4em",
        min_height="190px",
        justify="center",
        align="center",
        spacing="3",
    )


def links() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            section_header("Catálogo Dentcive", "Ver catálogo", "/catalogo"),
            rx.grid(
                rx.foreach(
                    State.products,
                    lambda p: product_card(p),
                ),
                columns=rx.breakpoints(initial="1", sm="2", md="4"),
                spacing="4",
                width="100%",
                id="productos",
            ),
            width="100%",
            spacing="4",
        ),
        rx.vstack(
            section_header("Especialidades", "Contactar", "#contacto"),
            rx.grid(
                category_card("Productos dentales", "shopping-bag"),
                category_card("Equipamiento", "monitor-cog"),
                category_card("Servicio técnico", "wrench"),
                category_card("Reparación rotatorio", "rotate-cw"),
                category_card("Mantenimiento", "settings"),
                category_card("Reforma clínica", "building-2"),
                category_card("Laboratorio", "microscope"),
                category_card("Consumibles", "package"),
                columns=rx.breakpoints(initial="2", md="4"),
                spacing="4",
                width="100%",
            ),
            width="100%",
            spacing="4",
            padding_top=Size.BIG.value,
        ),
        rx.vstack(
            rx.heading(
                "Distribuidores oficiales en España",
                size="6",
                color="#ffffff",
                text_align="center",
            ),
            rx.image(
                src="dentcive-logos-exclusivos.png",
                alt="Distribuidores oficiales Dentcive",
                max_width="760px",
                width="100%",
                height="auto",
            ),
            rx.text(
                "Como distribuidores oficiales estamos autorizados para vender y realizar el mantenimiento de productos de las marcas representadas.",
                color="#ffffff",
                text_align="center",
                max_width="780px",
            ),
            background_color="#093372",
            border_radius="4px",
            padding=rx.breakpoints(initial="2em 1em", md="3em"),
            width="100%",
            align="center",
            spacing="4",
            id="marcas",
        ),
        rx.grid(
            trust_card(
                "Precio",
                "Negociamos con fabricantes para ofrecer descuentos competitivos.",
                "badge-euro",
                Color.PRIMARY.value,
            ),
            trust_card(
                "Facilidad",
                "Más de 20.000 productos dentales con stock actualizado.",
                "boxes",
                Color.SECONDARY.value,
            ),
            trust_card(
                "Confianza",
                "Más de 2.000 clínicas dentales ya confían en Dentcive.",
                "shield-check",
                Color.PRIMARY.value,
            ),
            trust_card(
                "Cercanía",
                "Acompañamiento comercial y técnico con trato personalizado.",
                "handshake",
                Color.SECONDARY.value,
            ),
            columns=rx.breakpoints(initial="1", sm="2", md="4"),
            spacing="0",
            width="100%",
            id="nosotros",
        ),
        rx.flex(
            rx.vstack(
                rx.heading("¿Quieres abrir o reformar tu clínica?", size="6", color=TextColor.HEADER.value),
                rx.text(
                    "Dentcive ofrece asesoramiento para nuevas clínicas, reformas, mantenimiento y restauración de equipamiento.",
                    color=TextColor.BODY.value,
                ),
                align_items="start",
                spacing="2",
            ),
            rx.link(
                rx.button(rx.icon(tag="send", size=20), "Solicita información", size="3"),
                href="mailto:dentcive@gmail.com?subject=Solicitud%20de%20informacion%20Dentcive",
            ),
            flex_direction=rx.breakpoints(initial="column", md="row"),
            align=rx.breakpoints(initial="start", md="center"),
            justify="between",
            gap="1em",
            width="100%",
            background_color=Color.ACCENT.value,
            border_radius="4px",
            padding="1.5em",
            id="contacto",
        ),
        width="100%",
        spacing="6",
    )
