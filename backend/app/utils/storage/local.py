from typing import Optional
import base64
import time

from fastapi import File, UploadFile
import orjson
import qrcode

from app.core.config import settings
from app.utils.storage.base import BaseStorage, ImageModelType, QrCodeModelType
from app.utils.tools import FileTool


class LocalStorge(BaseStorage):
    async def save_image(
        self,
        instance: ImageModelType,
        image: UploadFile = File(None),
        size: Optional[tuple[int, int]] = None,
    ):
        if not image:
            return

        file = await image.read()
        path = f'/static/{instance.get_folder_name()}/{instance.id}/{time.time()}_image_{image.filename}'
        img_obj = self.valid_image(image=file)

        if size:
            file = self.resize(image=img_obj, size=size)

        await FileTool.save(path=f'.{path}', file=file)
        instance.set_file_value(value=path)

    async def remove_image(self, instance: ImageModelType):
        path = instance.get_file_value()
        await FileTool.remove(path=path)

    async def save_qrcode(self, instance: QrCodeModelType):
        path = f'/static/{instance.get_folder_name()}/{instance.id}/qrcode.png'
        data = {
            'id': str(instance.id),
            'project': settings.project,
        }
        image = qrcode.make(base64.b64encode(orjson.dumps(data)))
        image.save(f'.{path}', kind='png', dark='#000000', light=None)

        instance.set_qrcode_value(value=path)

    async def remove_qrcode(self, instance: QrCodeModelType):
        path = instance.get_qrcode_value()
        await FileTool.remove(path=path)
