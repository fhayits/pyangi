from webob import Request, Response
from parse import parse
import inspect
import requests
import wsgiadapter
from jinja2 import Environment, FileSystemLoader
import os
from whitenoise import WhiteNoise


class Pyangi:
    def __init__(self, templates_dir="templates", static_dir="static"):
        self.routes = dict()

        self.template_env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_dir))
        )
        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)

    def __call__(self, environ, start_response):
        return self.whitenoise(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)


    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(request)

        if handler is not None:
            if inspect.isclass(handler):
                handler_method = getattr(handler(), request.method.lower(), None)


                if handler_method is None:
                    response.status_code = 405
                    response.text = "Method not allowed"
                    return response

                handler_method(request, response, **kwargs)
            else:
                handler(request, response, **kwargs)
        else:
            self.default_response(response)
        return response

    def add_route(self, path, handler):
        assert path not in self.routes, "Duplicate error. Please change the URL"
        self.routes[path] = handler


    def find_handler(self, request):
        for path, handler in self.routes.items():
            parsed_result = parse(path, request.path)
            if parsed_result is not None:
                return handler, parsed_result.named
        return None, {}


    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."

    def route(self, path):
        # if path in self.routes: raise AssertionError("Duplicate handler. Please change the URL")
        # assert path not in self.routes, "Duplicate error. Please change the URL"
        def wrapper(handler):
            self.add_route(path, handler)
            return handler
        return wrapper

    def test_session(self):
        session = requests.Session()
        session.mount("http://test", wsgiadapter.WSGIAdapter(self))
        return session

    def template(self, template_name, context=None):
        if context is None:
            context = {}
        return self.template_env.get_template(template_name).render(**context).encode()


