import reflex as rx
from link_bio.components.links_button import links_button
from link_bio.components.Tilulos import title


def links() -> rx.Component:
    return rx.vstack(
        title("Estos son mis enlaces",),
        links_button("Youtube", "https://www.youtube.com/@jeffersoncanizares8486","youtube" ),
        links_button("Amazon","https://www.amazon.es/","store" ),
        links_button("Twitch", "https://www.twitch.tv/teenwolfw","twitch" ),
        links_button("Linkedin", "https://www.linkedin.com/feed/?trk=guest_homepage-basic_nav-header-signin","briefcase" ),
        links_button("Instagram", "https://www.instagram.com/","camera"),
        width="100%",
        spacing="4",

    ),
