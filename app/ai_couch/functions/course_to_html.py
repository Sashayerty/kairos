import markdown


def convert_course_to_html(course: dict) -> dict:
    """Конвертирует курс из markdown в html"""
    for key in course.keys():
        converter = markdown.Markdown(
            extensions=["nl2br", "fenced_code", "codehilite"]
        )
        course[key]["data"] = converter.convert(course[key]["data"])
        converter.reset()
    return course
