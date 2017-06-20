from nio.block.base import Block
from nio.signal.base import Signal
from nio.command import command
from nio.command.params.dict import DictParameter
from nio.properties import IntProperty, ObjectProperty, PropertyHolder, \
    StringProperty
from nio.modules.web import RESTHandler, WebEngine


class BuildSignal(RESTHandler):
    def __init__(self, endpoint, notify_signals, logger, response_headers):
        super().__init__('/'+endpoint)
        self.notify_signals = notify_signals
        self.logger = logger
        self.response_headers = response_headers

    def on_post(self, req, rsp):
        rsp.set_header('Access-Control-Allow-Origin',
                       self.response_headers().access_control_allow_origin())
        body = req.get_body()
        if isinstance(body, dict):
            body = [body]
        elif isinstance(body, list):
            pass
        else:
            self.logger.error(
                "Invalid JSON in PostSignal request body: {}".format(body))
            return
        signals = [Signal(s) for s in body]
        self.notify_signals(signals)

    def on_options(self, req, rsp):
        """Handle OPTIONS for CORS requests"""
        rsp.set_header('Access-Control-Allow-Origin',
                       self.response_headers().access_control_allow_origin())
        rsp.set_header('Access-Control-Allow-Headers',
                       self.response_headers().access_control_allow_headers())


class ResponseHeaders(PropertyHolder):
    access_control_allow_origin = StringProperty(
        title='Access-Control-Allow-Origin', default='*')
    access_control_allow_headers = StringProperty(
        title='Access-Control-Allow-Headers',
        default='Accept, Origin, Content-Type, Authorization')


@command("post", DictParameter("signal"))
class PostSignal(Block):

    host = StringProperty(title='Host', default='0.0.0.0')
    port = IntProperty(title='Port', default=8182)
    endpoint = StringProperty(title='Endpoint', default='')
    response_headers = ObjectProperty(
        ResponseHeaders, title='Response Headers', default=ResponseHeaders())

    def __init__(self):
        super().__init__()
        self._server = None
        self._signals = []

    def configure(self, context):
        super().configure(context)
        self._server = WebEngine.add_server(self.port(), self.host())
        self._server.add_handler(
            BuildSignal(self.endpoint(),
                        self.notify_signals,
                        self.logger,
                        self.response_headers),
        )

    def start(self):
        super().start()
        self._server.start()

    def stop(self):
        self._server.stop()
        super().stop()

    def post(self, sig):
        self.notify_signals([Signal(sig)])
