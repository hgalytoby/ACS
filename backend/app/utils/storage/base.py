from abc import ABCMeta, abstractmethod
from typing import Optional, Protocol
from uuid import UUID
import io

from PIL import Image, UnidentifiedImageError
from PIL.ImageFile import ImageFile
from fastapi import File, HTTPException, UploadFile, status

from app.core.config import logger
from app.utils.enums import AllowedImageExtensions, ImageFailDetail


class ImageModelType(Protocol):
    id: UUID | str

    def get_file_value(self) -> str:
        ...

    def get_folder_name(self) -> str:
        ...

    def set_file_value(self, value):
        ...


class QrCodeModelType(ImageModelType, Protocol):
    def get_qrcode_value(self) -> str:
        ...

    def set_qrcode_value(self, value):
        ...


class BaseStorage(metaclass=ABCMeta):
    @classmethod
    def valid_image(cls, image: str | bytes | ImageFile) -> ImageFile:
        match image:
            case bytes():
                image = io.BytesIO(image)
                open_image = Image.open(image)
            case str():
                open_image = Image.open(image)
            case Image():
                open_image = image
            case _:
                raise ValueError('valid_image image error')

        try:
            copy_img = open_image.copy()
            copy_img.verify()
            image_type = open_image.format.lower()
            if not AllowedImageExtensions.valid(type_=image_type):
                raise TypeError
            return open_image
        except (FileNotFoundError, UnidentifiedImageError, TypeError) as e:
            logger.info(f'valid_image error: {e}')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ImageFailDetail.INVALID_IMAGE_FORMAT,
            )

    @classmethod
    def resize(cls, image: ImageFile, size: tuple[int, int]) -> bytes:
        buffer = io.BytesIO()
        if image.mode == 'P':
            image = image.convert('RGB')
        image.thumbnail(size=size)
        image.save(buffer, format=image.format.lower())
        return buffer.getvalue()

    @abstractmethod
    async def save_image(
        self,
        instance: ImageModelType,
        image: UploadFile = File(None),
        size: Optional[tuple[int, int]] = None,
    ):
        raise NotImplementedError()

    @abstractmethod
    async def remove_image(self, instance: ImageModelType):
        raise NotImplementedError()

    @abstractmethod
    async def save_qrcode(self, instance: QrCodeModelType):
        raise NotImplementedError()

    @abstractmethod
    async def remove_qrcode(self, instance: QrCodeModelType):
        raise NotImplementedError()
