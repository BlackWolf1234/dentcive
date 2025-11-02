import reflex as rx
from link_bio.styles.styles import Size as Size
import link_bio.styles.styles as style 
from link_bio.styles.colors import Color as Color


def navbar() -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.text.span("Jeffer",color=Color.PRIMARY), 
            rx.text.span("son",color=Color.SECONDARY),
            style=style.navbar_title_style,
            ),
           
        position="sticky",
        bg=Color.CONTENT.value,
        padding_x=Size.BIG.value,
        padding_y=Size.SMALL.value,
        z_index="999",
        top="0",
        
    )
