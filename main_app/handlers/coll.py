import json

import numpy as np
import requests
from tornado.options import options
from indicoio import IndicoError
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
		try:
			if data_type == "text":
				labels = coll.predict("a").keys()
			elif data_type == "image":
				labels = coll.predict(np.array([[0]])).keys()
		except IndicoError as e:
			if e.message.endswith("does not exist.") or e.message.startswith("No trained model exists."):
				pass
			else:
				raise ValueError(e.message)
		return labels, coll

	def get(self, data_type, collection_name):
		labels, coll = self._details(data_type, collection_name)
		return self.render(
			"view.html",
			labels=labels,
			collection=coll,
			indico_api_key=options.indico_key,
		)

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
			previous_search = search,
			indico_api_key=options.indico_key,
		)

class TrainCollectionHandler(BaseHandler):
	def get(self, collection_name):
		collection = Collection(collection_name, api_key=options.indico_key)
		collection.train()
		collection.wait()
		origin_url = self.request.headers.get('Referer')
		self.redirect('/' + '/'.join(origin_url.split('/')[3:]))

class NewCollectionHandler(BaseHandler):
	def get(self):
		self.render("new.html")

	def post(self):
		new_collection_name = self.get_argument('newName')
		data_type = self.get_argument('dataType')
		self.redirect('/collection/%s/%s' % (data_type, new_collection_name))
