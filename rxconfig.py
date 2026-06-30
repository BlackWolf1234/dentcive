import reflex as rx


def _plugin(name: str):
    plugin = getattr(rx.plugins, name, None)
    return plugin() if plugin else None


plugins = [
    plugin
    for plugin in (
        _plugin("SitemapPlugin"),
        _plugin("TailwindV4Plugin"),
        _plugin("RadixThemesPlugin"),
    )
    if plugin is not None
]


config = rx.Config(
    app_name="dentcive",
    # Reflex uses frontend_path to prefix generated asset and route URLs.
    frontend_path="/dentcive",
    deploy_url="https://blackwolf1234.github.io/dentcive",
    plugins=plugins,
    upload_dir="uploaded_files",
)
