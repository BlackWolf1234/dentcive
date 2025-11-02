import reflex as rx
from enum import Enum
from link_bio.styles.colors import Color as Color
from link_bio.styles.colors import TextColor as TextColor
from link_bio.styles.fonts import Font as Fonts

# Constantes

MAX_WIDTH = "600px"

# Tamaños


class Size(Enum):
    Zero = "0px !important",
    SMALL = "0.5em",
    MEDIUM = "0.75em",
    DEFAULT = "1em",
    PESRNAL = "1.5em",
    BIG = "2em",

# styles


BASE_STYLE = {
    "font_family" : Fonts.DEFECTO.value,
    "background_color": Color.BACKGROUND.value,
    rx.button: {
        "_color": "gray",
        "width": "100%",
        "height": "100%",
        "padding": Size.DEFAULT.value,
        "border_radius": Size.BIG.value,
        "opacity": "90%",
        "display": "block",
        "border": "2px solid Gray",
        "background_color": Color.CONTENT.value,
        "_hover": {
            "background_color": Color.SECONDARY.value,
        }
    }
}


navbar_title_style = dict(
    font_family=Fonts.LOGO.value,
    font_size=Size.PESRNAL.value,
)


button_title_style = dict(
    font_size=Size.BIG.value,
    color=TextColor.HEADER.value,
       font_family = Fonts.TITLE,
)
button_body_style = dict(
    font_size=Size.DEFAULT.value,
    color=TextColor.BODY.value,
)

titulo_style = dict(
    color_scheme="cyan",
    padding_top=Size.DEFAULT.value,
    width="100%",
    text_align="left",
    font_family = Fonts.TITLE,
)
