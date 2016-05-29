from tornado.options import options
from indicoio.custom import Collection, collections

from handlers.base import BaseHandler

import logging
logger = logging.getLogger('boilerplate.' + __name__)


class DashboardHandler(BaseHandler):
    def get(self):
    	colls = collections(api_key=options.indico_key)
        self.render("dash.html", colls=colls)
