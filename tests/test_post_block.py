from collections import defaultdict
from unittest.mock import MagicMock
from nio.modules.threading import Event
from nio.util.support.block_test_case import NIOBlockTestCase
from ..post_block import PostSignal, BuildSignal


class PostSignalEvent(PostSignal):

    def __init__(self, e):
        super().__init__()
        self._e = e

    def notify_signals(self, signals, output_id='default'):
        super().notify_signals(signals, output_id)
        self._e.set()


class TestPostSignal(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        # This will keep a list of signals notified for each output
        self.last_notified = defaultdict(list)

    def signals_notified(self, signals, output_id='default'):
        self.last_notified[output_id].extend(signals)

    def _create_block(self, cfg, e):
        """ Create an instance of the block with a mocked web server """
        blk = PostSignalEvent(e)
        blk.configure_server = MagicMock()
        blk.start_server = MagicMock()
        blk.stop_server = MagicMock()
        self.configure_block(blk, cfg)
        return blk

    def test_defaults(self):
        e = Event()
        blk = self._create_block({}, e)
        blk.start()
        e.wait(0.1)
        blk.stop()

    def test_web_handler_post_dict(self):
        handler = BuildSignal(endpoint='',
                              notifier=self.signals_notified,
                              logger=MagicMock())
        request = MagicMock()
        request.get_body.return_value = {"I'm a": "dictionary"}
        handler.on_post(request, MagicMock())
        self.assertEqual(len(self.last_notified['default']), 1)
        self.assertDictEqual(self.last_notified['default'][0].to_dict(),
                             {"I'm a": "dictionary"})

    def test_web_handler_post_list(self):
        handler = BuildSignal(endpoint='',
                              notifier=self.signals_notified,
                              logger=MagicMock())
        request = MagicMock()
        request.get_body.return_value = [{"I'm a": "dictionary"},
                                         {"in a": "list"}]
        handler.on_post(request, MagicMock())
        self.assertEqual(len(self.last_notified['default']), 2)
        self.assertDictEqual(self.last_notified['default'][1].to_dict(),
                             {"in a": "list"})

    def test_web_handler_post_error(self):
        handler = BuildSignal(endpoint='',
                              notifier=self.signals_notified,
                              logger=MagicMock())
        request = MagicMock()
        request.get_body.return_value = "I'm just a string :("
        handler.on_post(request, MagicMock())
        self.assertEqual(len(self.last_notified['default']), 0)
