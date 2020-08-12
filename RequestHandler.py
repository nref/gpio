from GpioController import GpioController
from http.server import BaseHTTPRequestHandler

controller = GpioController()

class RequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args):
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_POST(self):
        response = self.route_post()
        self.wfile.write(response)

    def do_GET(self):
        response = self.route_get()
        self.wfile.write(response)

    def route_post(self):
        return self.route_anything(controller.get_post_routes)

    def route_get(self):
        return self.route_anything(controller.get_get_routes)

    def route_anything(self, get_routes):
        
        route = list(filter(None, self.path.split("/")))
        arg = self.parse_args(route)
        routes = get_routes(arg)

        if self.path not in routes:
            return self.not_found()
        try:
            if arg == -1: response = routes[self.path]()
            else:         response = routes[self.path](arg)
            
        except Exception as e:
            return self.bad_request(str(e))

        return self.ok(response)

    def parse_args(self, route):
        if len(route) < 2:
            return -1;

        try:
            return int(route[1])
        except ValueError:
            return -1

    def not_found(self):
        self.send_response(404)
        return bytes('Not Found\n', 'utf-8')

    def bad_request(self, response):
        self.send_response(400)
        return bytes(f'{response}\n', 'utf-8')

    def ok(self, response):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if response is None:
            response = 'ok'

        return bytes(f'{response}\n', 'utf-8')
