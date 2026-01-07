from open_ai import OpenAIImageEditor
from models import Models


def get_editor() -> OpenAIImageEditor:
    """
    Инициализация сервиса редактирования изображений
    """

    api_key = "sk-4vVvOJL5rzohB6itJunZQ7A7A5zxqipy"
    return OpenAIImageEditor(api_key=api_key)


def edit_single_image():
    """
    Пример редактирования одного изображения
    """
    editor = get_editor()

    editor.edit_image(
        prompt="Use the user's appearance 1:1 — the same face, skin tone, hair, face angle and proportions without any changes. Create a realistic photo of the user, the girl is lying on a massive wooden lacquered table. She is wearing an elegant beige corset, a white tunic on her hips, and white elbow-length gloves on her hands. With one hand, she leans on the table on which she is lying. There is a corner of the room behind it, and two Roman busts are located on opposite sides of the corner. The lighting is warm, slightly subdued with soft daylight. The atmosphere is elegant and cinematic. —v 6 —ar 3:4 —in raw format —q 2 —uplight —hd.",
        image_paths="input.jpg",
        output_path="output.png",
        model=Models.NANO_BANANA,
    )


def edit_multiple_images():
    """
    Пример редактирования нескольких изображений
    """
    editor = get_editor()

    editor.edit_image(
        prompt="Use the user's appearance 1:1 — the same face, skin tone, hair, face angle and proportions without any changes. Create a realistic photo of the user, the girl is lying on a massive wooden lacquered table. She is wearing an elegant beige corset, a white tunic on her hips, and white elbow-length gloves on her hands. With one hand, she leans on the table on which she is lying. There is a corner of the room behind it, and two Roman busts are located on opposite sides of the corner. The lighting is warm, slightly subdued with soft daylight. The atmosphere is elegant and cinematic. —v 6 —ar 3:4 —in raw format —q 2 —uplight —hd.",
        image_paths=[
            "image1.png",
            "image2.png",
        ],
        output_path="result.png",
        model=Models.OPEN_AI_LOW,
    )


def run_example():
    """
    Точка входа для быстрого теста
    """
    edit_single_image()
    # edit_multiple_images()


if __name__ == "__main__":
    run_example()
