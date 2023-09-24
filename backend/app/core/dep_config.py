import os

workers = os.environ.get('cpu', os.cpu_count() or 1)
worker_class = 'uvicorn.workers.UvicornWorker'
bind = '0.0.0.0:8000'
