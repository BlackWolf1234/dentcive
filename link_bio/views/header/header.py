import reflex as rx
from link_bio.components.links_icos import links_icon
from link_bio.components.info_text import info_text
from link_bio.styles.styles import Size as Size
from link_bio.styles.colors import TextColor as TextColor
from link_bio.styles.colors import Color as Color

def header() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.avatar(name="Jefferson",
                      src="F1.png",
                      color=TextColor.BODY.value,
                      bg=Color.CONTENT.value,
                      padding="2px",
                      border="4px",
                      border_color = Color.PRIMARY.value,
                      size="9",
                      radius="full"
                      ),

            rx.vstack(
                rx.text(
                    "Hola mi nombre es Jefferson Cañizares Mildestein",
                    size="4",
                    weight="bold",
                    color=TextColor.HEADER.value,
                ),
                rx.text("@jeffer",
                        margin_top=Size.Zero.value,
                        size="4"
                        ),
                rx.hstack(
                    links_icon("https://retosdeprogramacion.com/","braces"),
                    links_icon("https://reflex.dev/docs/getting-started/introduction/", "square-terminal"),
                    links_icon("https://github.com/mouredev/Hello-Python?tab=readme-ov-file", "book"),
                    links_icon("https://www.python.org/doc/", "parentheses"),
                ),
                align_items="start",
            ),
            spacing="5",
        ),
        rx.flex(rx.hstack(
            info_text(
                "+6 ","años de experiencia.",
            ),
            rx.spacer(),
            info_text(
                "SAT ", "Equipos dentales",
            ),
            rx.spacer(),
            info_text(
                "Reparaciones ","de maquinas dentales",

            ),
            witdh="100%",

        )),


        rx.text(
            """La mayoría de la gente se enfoca en comer perros, pero yo descubrí que la verdadera magia ocurre cuando comes gatos.""",
            color=TextColor.BODY.value,
        ),
        direction="column",
        spacing="6",
        align_items="start",

    ),
