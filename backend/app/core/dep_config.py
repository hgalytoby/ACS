import os

workers = os.environ.get('CPU', os.cpu_count() or 1)
worker_class = 'uvicorn.workers.UvicornWorker'
bind = '0.0.0.0:8000'
