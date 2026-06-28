import reflex as rx
from dentcive.styles.colors import Color
from dentcive.styles.styles import Size
from dentcive.state import State


def login_form() -> rx.Component:
    """Formulario de inicio de sesión con inputs controlados por el estado."""
    return rx.vstack(
        rx.heading("Dentcive", size="6", color=Color.PRIMARY.value, text_align="center"),
        # Input de email controlado: sincroniza con State.login_email
        rx.input(
            placeholder="Correo electrónico",
            type_="email",
            value=State.login_email,
            on_change=State.set_login_email,
            width="100%",
        ),
        # Input de contraseña controlado: sincroniza con State.login_password
        rx.input(
            placeholder="Contraseña",
            type_="password",
            value=State.login_password,
            on_change=State.set_login_password,
            width="100%",
        ),
        rx.button(
            "Iniciar sesión",
            width="100%",
            on_click=State.login,
        ),
        rx.text(
            "¿No tienes cuenta? ",
            rx.link(
                "Registrarse",
                href="#",
                color=Color.PRIMARY.value,
                on_click=State.toggle_register_modal,
            ),
            font_size="0.9em",
            text_align="center",
        ),
        spacing="3",
        align_items="stretch",
    )


def auth_modal() -> rx.Component:
    """Modal de autenticación (overlay fijo centrado en pantalla)."""
    return rx.cond(
        State.show_login_modal,
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.heading("Iniciar Sesión", size="5"),
                    rx.spacer(),
                    rx.button(
                        "✕",
                        on_click=State.toggle_login_modal,
                        background_color="transparent",
                        border="none",
                        font_size="1.5em",
                    ),
                    width="100%",
                    align="center",
                ),
                login_form(),
                spacing="4",
                padding="2em",
                background_color=Color.CONTENT.value,
                border_radius="8px",
                width="100%",
                max_width="400px",
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
