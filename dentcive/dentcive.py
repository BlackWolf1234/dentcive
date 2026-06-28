import reflex as rx

from dentcive.admin.admin_page import admin_page
from dentcive.components.auth_modal import auth_modal
from dentcive.components.cart_modal import cart_modal
from dentcive.components.wishlist_sidebar import wishlist_modal
from dentcive.components.footer import footer
from dentcive.components.navbar import navbar
from dentcive.state import State
from dentcive.styles.styles import Size as Size
import dentcive.styles.styles as styles
from dentcive.views.catalog.catalog import catalog_page
from dentcive.views.header.header import header
from dentcive.views.links.links import links
from dentcive.views.service.service import service_page
from dentcive.views.store.store import store_page


# ----------------------------------------------------------------- páginas


def index() -> rx.Component:
    """Landing pública con catálogo, hero y servicios."""
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(
                header(),
                links(),
                footer(),
                max_width=styles.MAX_WIDTH,
                width="100%",
                padding_x=Size.DEFAULT.value,
                margin_y=Size.BIG.value,
                align="center",
            ),
            width="100%",
        ),
        auth_modal(),
        cart_modal(),
        wishlist_modal(),
        on_mount=State.reload_products,
        padding_top=rx.breakpoints(initial="120px", md="155px"),
        overflow_x="hidden",
    )


# ------------------------------------------------------------------- app

app = rx.App(style=styles.BASE_STYLE)
app.add_page(index, route="/")
app.add_page(catalog_page, route="/catalogo")
app.add_page(service_page, route="/servicio-tecnico")
app.add_page(store_page, route="/tienda")
app.add_page(admin_page, route="/admin")
