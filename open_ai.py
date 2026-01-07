from typing import List, Union
import base64

from openai import OpenAI
from models import Models

class OpenAIImageEditor:
    """
    Класс для редактирования и генерации изображений
    через OpenAI Images API
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.proxyapi.ru/openai/v1",
    ):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    @staticmethod
    def _open_images(
        paths: Union[str, List[str]],
    ) -> List:
        """
        Открывает одно или несколько изображений в бинарном режиме
        """
        if isinstance(paths, str):
            paths = [paths]

        return [open(path, "rb") for path in paths]

    @staticmethod
    def _save_base64_image(
        image_base64: str,
        output_path: str,
    ) -> None:
        """
        Декодирует base64 и сохраняет изображение на диск
        """
        image_bytes = base64.b64decode(image_base64)

        with open(output_path, "wb") as f:
            f.write(image_bytes)

        print(f"Сохранено: {output_path}")

    def edit_image(
        self,
        prompt: str,
        image_paths: Union[str, List[str]],
        output_path: str,
        model: Models = Models.OPEN_AI_LOW,
    ) -> None:
        """
        Редактирует изображение(я) на основе prompt
        """
        images = self._open_images(image_paths)

        try:
            result = self.client.images.edit(
                model=model,
                image=images,
                prompt=prompt,
            )

            image_base64 = result.data[0].b64_json
            self._save_base64_image(image_base64, output_path)

        finally:
            # гарантированно закрываем файлы
            for img in images:
                img.close()
