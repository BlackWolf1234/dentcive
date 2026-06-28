import reflex as rx
from dentcive.styles.styles import Size as Size
from dentcive.styles.colors import TextColor as TextColor
from dentcive.styles.colors import Color as Color


def service_tile(title: str, body: str, icon: str, bg: str) -> rx.Component:
    return rx.vstack(
        rx.icon(tag=icon, size=34, color="#ffffff"),
        rx.heading(title, size="4", color="#ffffff", text_align="center", line_height="1.05"),
        rx.text(body, color="#ffffff", text_align="center", font_size="0.9em"),
        background_color=bg,
        padding="1.4em",
        min_height="210px",
        justify="center",
        align="center",
        spacing="3",
    )


def header() -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.heading(
                    "Productos dentales, equipamiento y servicio técnico",
                    size="8",
                    color="#ffffff",
                    text_align="center",
                    line_height="1.05",
                    max_width="820px",
                ),
                rx.text(
                    "Más de 25 años reparando, asesorando y acompañando a clínicas dentales.",
                    size="4",
                    color="#ffffff",
                    text_align="center",
                    max_width="720px",
                ),
                rx.hstack(
                    rx.link(
                        rx.button(rx.icon(tag="book-open", size=20), "Ver catálogo", size="3"),
                        href="/catalogo",
                    ),
                    rx.link(
                        rx.button(
                            rx.icon(tag="wrench", size=20),
                            "Servicio técnico",
                            size="3",
                            background_color=Color.ACCENT.value,
                            color="#111111",
                            _hover={"background_color": "#ffd84d"},
                        ),
                        href="#servicios",
                    ),
                    spacing="3",
                    wrap="wrap",
                    justify="center",
                ),
                min_height="430px",
                justify="center",
                align="center",
                spacing="5",
                padding=rx.breakpoints(initial="2em 1em", md="3em"),
                background="rgba(0, 0, 0, 0.55)",
            ),
            background_image="url('/dentcive-clinic-bg.jpg')",
            background_size="cover",
            background_position="center",
            border_radius="0",
            overflow="hidden",
            width="100%",
            id="inicio",
        ),
        rx.grid(
            service_tile(
                "ÁREA COMERCIAL",
                "Asesoramiento personalizado para elegir productos y equipamientos adecuados.",
                "briefcase-business",
                Color.PRIMARY.value,
            ),
            service_tile(
                "REPARACIÓN ROTATORIO",
                "Turbinas, contra-ángulos, piezas de mano, micromotores y acoplamientos.",
                "rotate-cw",
                Color.SECONDARY.value,
            ),
            service_tile(
                "SERVICIO TÉCNICO",
                "Reparación y solución de averías con respuesta fiable y eficiente.",
                "settings",
                Color.GRAPHITE.value,
            ),
            service_tile(
                "ASESORAMIENTO",
                "Reforma, mantenimiento, creación de clínicas y restauración de equipamiento.",
                "messages-square",
                "#333333",
            ),
            columns=rx.breakpoints(initial="1", sm="2", md="4"),
            spacing="0",
            width="100%",
            id="servicios",
        ),
        padding_y=Size.BIG.value,
        width="100%",
        spacing="6",
    )
