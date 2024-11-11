from components import style
import registrar
from routes import (
    basic_arithmetic,
    linear_equations,
    quadratic_equations
)

import os

import hyperdiv as hd


router = registrar.router


@router.route("/")
def index():
    hd.h1("Матема+").text_gradient = (0, hd.Color.neutral_800, hd.Color.neutral_900)

    style.underlined(
        hd.text(
            "Вчися просто — досягай більше з «Матема+»!",
            margin=3, font_size=hd.FontSize.large
        )
    )

    hd.text(
        "«Матема+» — інтерактивний генератор математичних завдань."
    )
    
    hd.h2("Для учнів", margin=(2, 0, 2, 0))
    
    style.underlined(
        hd.text(
            "Ви можете покращити свої практичні навички в математиці, розвʼязуючи "
            "різні типи завдань. ",
            margin_bottom=1
        )
    )
    
    hd.text(
        "«Матема+» дозволяє вам підібрати бажаний рівень складності під ваші потреби. "
        "На початку нової теми вам може знадобитись нижчий рівень складності, "
        "але з часом ви можете додавати ускладнення, або розвʼязувати завдання іншим "
        "способом. Ви можете використовувати цей генератор як необмежене джерело практики."
    )
    
    hd.h2("Для викладачів", margin=(2, 0, 2, 0))

    style.underlined(
        hd.text(
            "Ви можете краще визначити та підвищити рівень знань ваших учнів завдяки "
            "практичним завданням.",
            margin_bottom=1
        )
    )
    
    hd.text(
        "Під час вивчення нової теми важливо добре закріпити її на практиці. "
        "Буває складно вручну створювати велику кількість завдань, які до того ж мають "
        "відповідати чітким правилам та добре підходити під певний вид розвʼязку. "
        "Замість цього ви можете використати цей генератор для отримання безмежної "
        "кількості практичного матеріалу для ваших занять."
    )
    
    hd.h5(
        "Для початку роботи оберіть генератор у потрібному розділі в меню зліва.",
        margin_top=4
    )


def sidebar(app: hd.template) -> None:
    with app.sidebar:
        with hd.hbox(gap=1, align="center"):
            hd.icon("gear", font_size=hd.FontSize.large)
            hd.text("Генератори", font_size=hd.FontSize.large)

    app.add_sidebar_menu(registrar.get_sidebar_menu())
    app.sidebar.background_color = hd.Color.neutral_50
    app.drawer.body_style = hd.style(background_color=hd.Color.neutral_50)


def topbar(app: hd.template) -> None:
    with app.topbar_links:
        with hd.breadcrumb(margin=(0, 2, 0, 1)):
            loc = hd.location().path
            names = registrar.get_names(loc)
            if names is not None:
                section_name, page_name = names
                hd.breadcrumb_item(section_name, href="#")
                hd.breadcrumb_item(page_name, href="#")


def content(app: hd.template, responsive_threshold: int) -> None:
    page_content_width_percentage = 70
    if hd.window().width < responsive_threshold:
        page_content_width_percentage = 85
        
    side_margin = f"{page_content_width_percentage // 2}%"

    app.body.align = "center"
    with app.body:
        with hd.box(
            width=f"{page_content_width_percentage}%", height="100vh",
            align="center", text_align="center"
        ):
            router.run()


def main() -> None:
    responsive_threshold = 1000
    
    app = hd.template(
        title="Матема+",
        sidebar=True,
        responsive_threshold=responsive_threshold
    )
    
    sidebar(app)
    topbar(app)
    content(app, responsive_threshold)


if __name__ == "__main__":
    os.environ["HD_PRODUCTION"] = "1"
    os.environ["HD_PRINT_OUTPUT"] = "0"
    os.environ["HD_HOST"] = "0.0.0.0"
    os.environ["HD_PORT"] = "8888"

    hd.run(
        main,
        index_page=hd.index_page(
            title="Матема+",
            css_assets=["/assets/index.css"],
            raw_head_content=(
                "<link rel=\"preload\" "
                "href=\"assets/e-Ukraine-Regular.woff\" "
                "as=\"font\" "
                "type=\"font/woff\" crossorigin />"
            )
        )
    )
