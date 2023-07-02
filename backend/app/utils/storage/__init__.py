from app.core.config import settings
from app.utils.enums import StorageType
from app.utils.storage.gcstorage import GCStorge
from app.utils.storage.local import LocalStorge

match settings.storage:
    case StorageType.LOCAL:
        Storage = LocalStorge()
    case StorageType.GCP:
        try:
            from app.core.config import GCStorage

            gc_storge = GCStorage()
            Storage = GCStorge(service_file=gc_storge.cert, bucket_name=gc_storge.BUCKET_NAME)
        except Exception as e:
            raise e
    case _:
        raise ValueError('無效的 StorageType')
