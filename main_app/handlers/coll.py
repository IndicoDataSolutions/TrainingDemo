import numpy as np
from tornado.options import options
from indicoio.custom import Collection

from handlers.base import BaseHandler

import logging
logger = logging.getLogger('boilerplate.' + __name__)


class DeleteCollectionHandler(BaseHandler):
	def get(self, collection_name):
		Collection(collection_name, api_key=options.indico_key).clear()
		self.redirect("/")

class ViewCollectionHandler(BaseHandler):
	def get(self, data_type, collection_name):
		coll = Collection(collection_name)
		labels = []
		if data_type == "text":
			labels = coll.predict("a").keys()
		elif data_type == "image":
			labels = coll.predict(np.array([[0]])).keys()
		return self.render("view.html", labels=labels, collection=coll)

# class CollectionSearchHandler(BaseHandler):
# 	def 

class TrainCollectionHandler(BaseHandler):
	def get(self):
		self.redirect("/")
