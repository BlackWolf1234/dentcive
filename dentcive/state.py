import reflex as rx
from typing import TypedDict, Any
from dentcive.data.products import COUPONS
from dentcive.utils.i18n import TRANSLATIONS as _TRANSLATIONS
import dentcive.admin.products_store as products_store


class LocalizedText(TypedDict):
    es: str
    en: str


class Product(TypedDict):
    id: str
    name: LocalizedText
    category: str
    subcategory: str
    price: float
    old_price: float
    image: str
    description: LocalizedText
    badge: str
    featured: bool
    brand: str
    tag: str
    price_str: str
    old_price_str: str
    wa_url: str
    budget_url: str
    brand_or_empty: str
    tag_or_empty: str


class State(rx.State):
    """Estado global de la aplicación."""

    # ---- Auth ----
    user_id: str = ""
    username: str = ""
    email: str = ""
    is_logged_in: bool = False
    login_email: str = ""
    login_password: str = ""

    # ---- Cart / Wishlist ----
    cart_items: list[dict[str, Any]] = []
    wishlist_ids: list[str] = []

    # ---- i18n / coupons ----
    language: str = "es"
    coupon_input: str = ""
    applied_coupon: str = ""
    coupon_discount: float = 0.0

    # ---- Modals ----
    show_login_modal: bool = False
    show_cart_modal: bool = False
    show_register_modal: bool = False
    show_wishlist_modal: bool = False

    # ---- Catálogo ----
    products: list[Product] = []
    catalog_pdfs: list[dict] = []

    # ---- Product detail ----
    current_product: dict = {}

    def load_product_page(self):
        self.reload_products()
        pid = self.router.page.params.get("pid", "")
        for p in self.products:
            if p["id"] == pid:
                self.current_product = p
                return
        self.current_product = {}

    # ---- Search ----
    search_query: str = ""

    # ---- Store filter ----
    store_filter_category: str = ""
    store_filter_subcategory: str = ""

    # ---- Computed: filtered products for store page ----

    @rx.var
    def filtered_store_products(self) -> list[Product]:
        result = self.products
        q = self.search_query.strip().lower()
        if q:
            result = [
                p for p in result
                if q in p.get("name", {}).get("es", "").lower()
                or q in p.get("name", {}).get("en", "").lower()
                or q in p.get("brand", "").lower()
                or q in p.get("category", "").lower()
            ]
        cat = self.store_filter_category
        sub = self.store_filter_subcategory
        if cat:
            result = [p for p in result if p.get("category") == cat]
        if sub:
            result = [p for p in result if p.get("subcategory") == sub]
        return result

    # ---- Store filter actions ----

    def set_store_filter_category(self, category: str):
        self.store_filter_category = category
        self.store_filter_subcategory = ""

    def set_store_filter_subcategory(self, subcategory: str):
        self.store_filter_subcategory = subcategory
        if subcategory:
            self.store_filter_category = "rotatorio"

    def clear_store_filter(self):
        self.store_filter_category = ""
        self.store_filter_subcategory = ""
        self.search_query = ""

    def set_search_query(self, value: str):
        self.search_query = value

    def do_search(self):
        query = self.search_query.strip()
        if query:
            return rx.redirect(f"/tienda?q={query}")

    def load_store_page(self):
        self.reload_products()
        params = self.router.page.params
        cat = params.get("cat", "")
        sub = params.get("sub", "")
        q = params.get("q", "")
        if q:
            self.search_query = q
        if cat:
            self.store_filter_category = cat
        if sub:
            self.store_filter_subcategory = sub

    # i18n computed

    @rx.var
    def translations(self) -> dict[str, str]:
        return {k: v.get(self.language, v.get("es", k)) for k, v in _TRANSLATIONS.items()}

    @rx.var
    def service_products(self) -> list[Product]:
        return [p for p in self.products if p.get("badge") == "Servicio" or p.get("tag") == "servicio"]

    # ---- Computed: cart ----

    @rx.var
    def cart_subtotal(self) -> float:
        return sum(
            float(item.get("qty", 0)) * float(item.get("price", 0.0))
            for item in self.cart_items
        )

    @rx.var
    def cart_discount_amount(self) -> float:
        return round(self.cart_subtotal * (self.coupon_discount / 100), 2)

    @rx.var
    def cart_total(self) -> float:
        return round(self.cart_subtotal - self.cart_discount_amount, 2)

    @rx.var
    def cart_subtotal_str(self) -> str:
        return f"${self.cart_subtotal:.2f}"

    @rx.var
    def cart_discount_str(self) -> str:
        return f"-${self.cart_discount_amount:.2f}"

    @rx.var
    def cart_total_str(self) -> str:
        return f"${self.cart_total:.2f}"

    # ---- Setters ----

    def set_login_email(self, value: str):
        self.login_email = value

    def set_login_password(self, value: str):
        self.login_password = value

    def set_coupon_input(self, value: str):
        self.coupon_input = value

    # ---- Catálogo ----

    def reload_products(self):
        self.products = products_store.load_products()

    def load_catalog_page(self):
        self.catalog_pdfs = products_store.list_pdfs()
        self.catalog_pdfs = [
            {**pdf, "url": "/" + pdf["file"]} for pdf in self.catalog_pdfs
        ]

    # ---- Wishlist ----

    def toggle_wishlist(self, product_id: str):
        if product_id in self.wishlist_ids:
            self.wishlist_ids.remove(product_id)
        else:
            self.wishlist_ids.append(product_id)

    # ---- Cart ----

    def add_to_cart(self, product_id: str, price: float, qty: int = 1):
        for item in self.cart_items:
            if item["product_id"] == product_id:
                item["qty"] += qty
                return
        self.cart_items.append({"product_id": product_id, "qty": qty, "price": price})

    def remove_from_cart(self, product_id: str):
        self.cart_items = [
            item for item in self.cart_items if item["product_id"] != product_id
        ]

    # ---- Coupons ----

    def apply_coupon(self):
        code = self.coupon_input.strip().upper()
        for coupon in COUPONS:
            if coupon["code"].upper() == code:
                self.applied_coupon = coupon["code"]
                self.coupon_discount = float(coupon["discount"])
                self.coupon_input = ""
                return

    def apply_coupon_code(self, code: str):
        for coupon in COUPONS:
            if coupon["code"].upper() == code.strip().upper():
                self.applied_coupon = coupon["code"]
                self.coupon_discount = float(coupon["discount"])
                return

    # ---- i18n ----

    def toggle_language(self):
        self.language = "en" if self.language == "es" else "es"

    # ---- Auth ----

    def login(self):
        if not self.login_email or not self.login_password:
            return
        self.is_logged_in = True
        self.user_id = f"user_{abs(hash(self.login_email)) % 100000:05d}"
        self.username = self.login_email.split("@")[0]
        self.email = self.login_email
        self.login_email = ""
        self.login_password = ""
        self.show_login_modal = False
        self.show_register_modal = False

    def logout(self):
        self.is_logged_in = False
        self.user_id = ""
        self.username = ""
        self.email = ""
        self.cart_items = []
        self.applied_coupon = ""
        self.coupon_discount = 0.0

    # ---- Modals ----

    def toggle_login_modal(self):
        self.show_login_modal = not self.show_login_modal

    def toggle_cart_modal(self):
        self.show_cart_modal = not self.show_cart_modal

    def toggle_register_modal(self):
        self.show_register_modal = not self.show_register_modal

    def toggle_wishlist_modal(self):
        self.show_wishlist_modal = not self.show_wishlist_modal
