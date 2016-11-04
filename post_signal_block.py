from nio.block.base import Block
from nio.signal.base import Signal
from nio.command import command
from nio.command.params.dict import DictParameter
from nio.properties.string import StringProperty
from nio.properties.int import IntProperty
from nio.modules.web import RESTHandler, WebEngine


class BuildSignal(RESTHandler):
    def __init__(self, endpoint, notify_signals, logger):
        super().__init__('/'+endpoint)
        self.notify_signals = notify_signals
        self.logger = logger

    def on_post(self, req, rsp):
        body = req.get_body()
        if isinstance(body, dict):
            body = [body]
        elif isinstance(body, list):
            pass
        else:
            self.logger.error("Invalid JSON in PostSignal request body")
            return
        signals = [Signal(s) for s in body]
        self.notify_signals(signals)

    def on_options(self, req, rsp):
        """Handle OPTIONS for CORS requests"""
        pass


@command("post", DictParameter("signal"))
class PostSignal(Block):

    host = StringProperty(title='Host', default='0.0.0.0')
    port = IntProperty(title='Port', default=8182)
    endpoint = StringProperty(title='Endpoint', default='')

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
                        self.logger),
        )

    def start(self):
        super().start()
        self._server.start()

    def stop(self):
        self._server.stop()
        super().stop()

    def post(self, sig):
        self.notify_signals([Signal(sig)])
