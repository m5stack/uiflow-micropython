package(
    "startup",
    (
        "__init__.py",
        "paper/__init__.py",
        "paper/app_base.py",
        "paper/framework.py",
        "paper/apps/app_list.py",
        "paper/apps/dev.py",
        "paper/apps/settings.py",
        "paper/apps/status_bar.py",
    ),
    base_path="..",
    opt=3,
)
