import reflex as rx
import datetime
from link_bio.styles.styles import Size as Size
from link_bio.styles.colors import TextColor as TextColor


def footer() -> rx.Component:
    return rx.vstack(
        rx.image(src="F3.png", 
                 width="5em", 
                 height="auto"),
        rx.link("Me gustan los mangos",
                href="https://www.youtube.com/@CancioName"),
        rx.text(
            f"Hola muy buenas a todo el que lea este mensaje, felíz día {datetime.date.today()}", align="left",
            font_size=Size.MEDIUM.value,),
        align="center",
        margin_bottom=Size.BIG.value,
        padding_top=Size.BIG.value,
        padding_bottom=Size.BIG.value,
        color=TextColor.BODY.value,

    )
