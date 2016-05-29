import json

import numpy as np
import requests
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

	def _details(self, data_type, collection_name):
		"""
		Helper function
		"""
		coll = Collection(collection_name)
		labels = []
		if data_type == "text":
			labels = coll.predict("a").keys()
		elif data_type == "image":
			labels = coll.predict(np.array([[0]])).keys()
		return labels, coll

	def get(self, data_type, collection_name):
		labels, coll = self._details(data_type, collection_name)
		return self.render("view.html", labels=labels, collection=coll)

	def post(self, data_type, collection_name):
		labels, coll = self._details(data_type, collection_name)
		search = self.get_argument("query")
		search_payload = {
			"key": options.pixabay_key,
			"q": search,
			"safesearch": True,
			"per_page": 100,
		}
		results = json.loads(requests.get("https://pixabay.com/api", params=search_payload).content)["hits"]
		search_results = [{"preview": result['previewURL'], "base": result["webformatURL"]} for result in results]

		self.render(
			"view.html",
			labels = labels,
			collection = coll,
			search_results = search_results,
			previous_search = search
		)

# class CollectionSearchHandler(BaseHandler):
# 	def 

class TrainCollectionHandler(BaseHandler):
	def get(self):
		self.redirect("/")
