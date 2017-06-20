from unittest.mock import MagicMock, patch
from nio.block.terminals import DEFAULT_TERMINAL
from nio.testing.block_test_case import NIOBlockTestCase
from ..post_signal_block import PostSignal, BuildSignal


class TestPostSignal(NIOBlockTestCase):

    def notify_signals(self, signals):
        """Use as callback for handler without needing a block in the test."""
        with patch(PostSignal.__module__ + ".WebEngine"):
            blk = PostSignal()
            self.configure_block(blk, {})
            blk.notify_signals(signals)

    def test_web_handler_post_dict(self):
        handler = BuildSignal(endpoint='',
                              notify_signals=self.notify_signals,
                              logger=MagicMock(),
                              response_headers=MagicMock())
        request = MagicMock()
        request.get_body.return_value = {"I'm a": "dictionary"}
        handler.on_post(request, MagicMock())
        self.assertEqual(len(self.last_notified[DEFAULT_TERMINAL]), 1)
        self.assertDictEqual(self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
                             {"I'm a": "dictionary"})

    def test_web_handler_post_list(self):
        handler = BuildSignal(endpoint='',
                              notify_signals=self.notify_signals,
                              logger=MagicMock(),
                              response_headers=MagicMock())
        request = MagicMock()
        request.get_body.return_value = [{"I'm a": "dictionary"},
                                         {"in a": "list"}]
        handler.on_post(request, MagicMock())
        self.assertEqual(len(self.last_notified[DEFAULT_TERMINAL]), 2)
        self.assertDictEqual(self.last_notified[DEFAULT_TERMINAL][1].to_dict(),
                             {"in a": "list"})

    def test_web_handler_post_error(self):
        handler = BuildSignal(endpoint='',
                              notify_signals=self.notify_signals,
                              logger=MagicMock(),
                              response_headers=MagicMock())
        request = MagicMock()
        request.get_body.return_value = "I'm just a string :("
        handler.on_post(request, MagicMock())
        self.assertEqual(len(self.last_notified[DEFAULT_TERMINAL]), 0)

    def test_web_handler_options(self):
        handler = BuildSignal(endpoint='',
                              notify_signals=self.notify_signals,
                              logger=MagicMock(),
                              response_headers=MagicMock())
        handler.on_options(MagicMock(), MagicMock())
        self.assertEqual(len(self.last_notified[DEFAULT_TERMINAL]), 0)
