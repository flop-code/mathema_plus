from typing import Callable, Any, Annotated, Literal, TypeAlias

import hyperdiv as hd


PageRegisterType: TypeAlias = dict[
    Annotated[str, "section href"],
    tuple[
        Annotated[str, "section name"],
        dict[
            Annotated[str, "page href"],
            Annotated[str, "page name"]
        ]
    ]
]
SidebarMenuType: TypeAlias = dict[
    Annotated[str, "section name"],
    dict[
        Annotated[str, "page name"],
        dict[
            Literal["href"],
            Annotated[str, "full page href"]
        ]
    ]
]


_page_register: PageRegisterType = {}
router = hd.router()


@router.not_found
def not_found_page():
    with hd.box(gap=3, margin_top=0, width="100%", height="90%", align="center", justify="center"):
        hd.h2("Сторінка не знайдена.")
        hd.text(
            "Використайте меню зліва для переходу на існуючі сторінки, "
            "або натисність на логотип у лівому верхньому кутку для повернення "
            "на головну сторінку."
        )


def registrar(section_name: str, section_href: str) -> Callable:
    if _page_register.get(section_href) is None:
        _page_register[section_href] = (section_name, {})

    def wrapper(page_name: str) -> Callable:
        def wrapper2(func: Callable) -> Callable:
            router.route(f"/{section_href}/{func.__name__}")(func)
            _page_register[section_href][1][func.__name__] = page_name

            return func

        return wrapper2
    return wrapper


def get_sidebar_menu() -> SidebarMenuType:
    sidebar_menu: SidebarMenuType = {}

    for section_href, (section_name, pages) in _page_register.items():
        if sidebar_menu.get(section_name) is None:
            sidebar_menu[section_name] = {}

        for page_href, page_name in pages.items():
            sidebar_menu[section_name][page_name] = {"href": f"/{section_href}/{page_href}"}

    return sidebar_menu


def get_names(href: str) -> tuple[str, str] | None:
    if "/" not in href[1:]:
        return None

    section_href, page_href = href[1:].split("/")

    section = _page_register.get(section_href)
    if section is None or page_href not in section[1]:
        return None

    section_name = section[0]
    page_name = section[1][page_href]

    return section_name, page_name
