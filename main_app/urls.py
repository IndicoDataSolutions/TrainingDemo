from tornado.web import StaticFileHandler

from handlers.dash import DashboardHandler
from handlers.coll import ViewCollectionHandler, DeleteCollectionHandler, TrainCollectionHandler
from settings import settings

url_patterns = [
    (r"/", DashboardHandler),
    (r"/delete/([^/]+)", DeleteCollectionHandler),
    (r"/collection/([^/]+)/([^/]+)", ViewCollectionHandler),
    (r"/train/([^/]+)", TrainCollectionHandler),
    (r"/media/(.*)", StaticFileHandler, dict(path=settings["static_path"])),
]
