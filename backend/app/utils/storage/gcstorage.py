from dataclasses import dataclass
from typing import Optional
import base64
import io
import time

from fastapi import File, UploadFile
from gcloud.aio.storage import Storage
import orjson
import qrcode

from app.core.config import settings
from app.utils.storage.base import BaseStorage, ImageModelType, QrCodeModelType


@dataclass
class BlobMetadata:
    name: str
    link: str


class GCStorge(BaseStorage):
    def __init__(self, service_file: str, bucket_name: str):
        self.__storage_client = Storage(service_file=service_file)
        self.__bucket_name = bucket_name
        self.__host = 'https://storage.googleapis.com'

    async def upload_file(
        self,
        file_data: bytes,
        filename: str,
    ) -> BlobMetadata:
        metadata = await self.__storage_client.upload(
            bucket=self.__bucket_name,
            object_name=filename,
            file_data=file_data,
        )
        blob_metadata = BlobMetadata(
            name=metadata['name'],
            link=f'{self.__host}/{self.__bucket_name}/{filename}',
        )
        return blob_metadata

    async def delete_file(self, blob_name: str):
        await self.__storage_client.delete(
            bucket=self.__bucket_name,
            object_name=blob_name,
        )

    def link_to_filename(self, filename: str) -> str:
        return filename.replace(f'{self.__host}/{self.__bucket_name}/', '')

    async def save_image(
        self,
        instance: ImageModelType,
        image: UploadFile = File(None),
        size: Optional[tuple[int, int]] = None,
    ):
        if not image:
            return

        image_name = f'{instance.get_folder_name()}/{instance.id}/{time.time()}_image_{image.filename}'
        file = await image.read()
        image_obj = self.valid_image(image=file)

        if size:
            file = self.resize(image=image_obj, size=size)

        metadata = await self.upload_file(file_data=file, filename=image_name)
        instance.set_file_value(value=metadata.link)

    async def remove_image(self, instance: ImageModelType):
        blob_name = instance.get_file_value()
        await self.delete_file(blob_name=blob_name)

    async def save_qrcode(self, instance: QrCodeModelType):
        buffer = io.BytesIO()
        data = {
            'id': str(instance.id),
            'project': settings.project,
        }

        image = qrcode.make(base64.b64encode(orjson.dumps(data)))
        image.save(buffer, kind='png', dark='#000000', light=None)

        metadata = await self.upload_file(
            file_data=buffer.getvalue(),
            filename=f'{instance.get_folder_name()}/{instance.id}/qrcode.png',
        )

        instance.set_qrcode_value(value=metadata.link)

    async def remove_qrcode(self, instance: QrCodeModelType):
        blob_name = instance.get_qrcode_value()
        await self.delete_file(blob_name=blob_name)
