
import os
from server import make_worker

worker = make_worker(os.getenv("FLASK_CONFIG") or "default",)