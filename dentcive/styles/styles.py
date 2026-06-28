import reflex as rx
from enum import Enum
from dentcive.styles.colors import Color as Color
from dentcive.styles.colors import TextColor as TextColor
from dentcive.styles.fonts import Font as Fonts

# Constantes

MAX_WIDTH = "1240px"

# Tamaños


class Size(Enum):
    Zero = "0px !important"
    SMALL = "0.5em"
    MEDIUM = "0.75em"
    DEFAULT = "1em"
    PERSONAL = "1.5em"
    BIG = "2em"


# styles


BASE_STYLE = {
    "font_family": Fonts.DEFECTO.value,
    "font_weight": "500",
    "background_color": Color.BACKGROUND.value,
    "color": TextColor.BODY.value,
    rx.button: {
        "border_radius": "10px",
        "font_weight": "600",
        "cursor": "pointer",
        "transition": "all 200ms cubic-bezier(0.4, 0, 0.2, 1)",
        "border": "none",
        "background_color": Color.PRIMARY.value,
        "color": "#ffffff",
        "padding": "0.75em 1.5em",
        "box_shadow": "0 1px 3px 0 rgba(0, 0, 0, 0.1)",
        "_hover": {
            "background_color": Color.SECONDARY.value,
            "box_shadow": "0 4px 12px 0 rgba(37, 99, 235, 0.3)",
            "transform": "translateY(-1px)",
        },
    },
    rx.link: {
        "text_decoration": "none",
        "_hover": {
            "text_decoration": "none",
        },
    },
}


navbar_title_style = dict(
    font_family=Fonts.LOGO.value,
    font_size="1.1em",
    font_weight="700",
    letter_spacing="0.5px",
)


button_title_style = dict(
    font_size=Size.DEFAULT.value,
    color=TextColor.HEADER.value,
    font_family=Fonts.TITLE.value,
)
button_body_style = dict(
    font_size=Size.DEFAULT.value,
    color=TextColor.BODY.value,
)

titulo_style = dict(
    color=TextColor.HEADER.value,
    padding_top=Size.DEFAULT.value,
    width="100%",
    text_align="left",
    font_family=Fonts.TITLE.value,
)
