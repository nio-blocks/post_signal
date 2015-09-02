from unittest.mock import MagicMock
from nio.modules.threading import Event
from nio.util.support.block_test_case import NIOBlockTestCase
from ..post_block import PostSignal


class PostSignalEvent(PostSignal):

    def __init__(self, e):
        super().__init__()
        self._e = e

    def notify_signals(self, signals, output_id='default'):
        super().notify_signals(signals, output_id)
        self._e.set()


class TestPostSignal(NIOBlockTestCase):

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
        e.wait(1)
        blk.stop()
