import json

import tornado.web
from jinja2 import Environment, PackageLoader

import logging
logger = logging.getLogger('boilerplate.' + __name__)

class JinjaRendering(object):
    """
    Helper class for replacing tornado's rendering engine
    """
    def render_template(self, template_name, **kwargs):
        env = Environment(loader=PackageLoader("app"))

        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        content = template.render(**kwargs)
        return content

class BaseHandler(tornado.web.RequestHandler, JinjaRendering):
    """
    A class to collect common handler methods - all other handlers should
    subclass this one.
    """

    def load_json(self):
        """Load JSON from the request body and store them in
        self.request.arguments, like Tornado does by default for POSTed form
        parameters.

        If JSON cannot be decoded, raises an HTTPError with status 400.
        """
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            msg = "Could not decode JSON: %s" % self.request.body
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

    def get_json_argument(self, name, default=None):
        """Find and return the argument with key 'name' from JSON request data.
        Similar to Tornado's get_argument() method.
        """
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            logger.debug("Returning default argument %s, as we couldn't find "
                    "'%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        logger.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg

    def render(self, template_name, **kwargs):
        """
        Overwriting base tornado rendering with jinja2
        """
        content = self.render_template(template_name, **kwargs)
        self.write(content)
