import markdown


def convert_course_to_html(course: dict) -> dict:
    """Конвертирует курс из markdown в html

    Args:
        course (dict): Курс с пунктами в md

    Returns:
        dict: Курс с пунктами в html
    """
    for key in course.keys():
        converter = markdown.Markdown(
            extensions=["nl2br", "extra", "codehilite"]
        )
        course[key]["content"] = converter.convert(course[key]["content"])
        converter.reset()
    return course
