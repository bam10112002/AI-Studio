from io import BytesIO
from typing import List, Union

from PIL import Image
from google import genai
from google.genai import types
from models import Models


class GeminiImageEditor:
    """
    Класс для генерации и редактирования изображений
    с помощью Google Gemini (Image models)
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.proxyapi.ru/google",
    ):
        self.client = genai.Client(
            api_key=api_key,
            http_options={"base_url": base_url},
        )

    @staticmethod
    def _load_single_image(path: str) -> types.Blob:
        """
        Загружает одно изображение и конвертирует в Blob
        """
        image = Image.open(path)

        buffer = BytesIO()
        image.save(buffer, format="PNG")

        return types.Blob(mime_type="image/png", data=buffer.getvalue())

    def load_images(
        self,
        paths: Union[str, List[str]],
    ) -> List[types.ImageInput]:
        """
        Загружает одно или несколько изображений
        """
        if isinstance(paths, str):
            paths = [paths]

        return [self._load_single_image(path) for path in paths]

    def generate_image(
        self,
        prompt: str,
        image_paths: Union[str, List[str]],
        output_path: str,
        model: Models = Models.NANO_BANANA,
        aspect_ratio: str = "1:1",
    ) -> None:
        """
        Генерирует изображение на основе одного или нескольких входных изображений
        """
        response = self.client.models.generate_content(
            model=model.value,
            contents=prompt,
            image_inputs=self.load_images(image_paths),
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio
                ),
            ),
        )

        self._save_response_images(response, output_path)

    @staticmethod
    def _save_response_images(response, output_path: str) -> None:
        """
        Сохраняет изображения из ответа модели
        """
        for index, part in enumerate(response.parts):
            if part.inline_data:
                image = part.as_image()

                # если модель вернула несколько изображений
                if len(response.parts) > 1:
                    path = output_path.replace(
                        ".png", f"_{index + 1}.png"
                    )
                else:
                    path = output_path

                image.save(path)
                print(f"Сохранено: {path}")
