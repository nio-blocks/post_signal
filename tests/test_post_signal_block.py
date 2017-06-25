from unittest.mock import MagicMock, patch, ANY
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

    def test_web_handler_post_with_headers(self):
        handler = BuildSignal(endpoint='',
                              notify_signals=self.notify_signals,
                              logger=MagicMock(),
                              response_headers=MagicMock(),
                              include_headers=True)
        request = MagicMock()
        request.get_body.return_value = {"I'm a": "dictionary"}
        request.get_headers.return_value = {"we": "are", "the": "headers"}
        handler.on_post(request, MagicMock())
        self.assertEqual(len(self.last_notified[DEFAULT_TERMINAL]), 1)
        self.assertDictEqual(self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
                             {"I'm a": "dictionary",
                              "headers": {"we": "are", "the": "headers"}})

    def test_block_propertes_are_passed_to_handler(self):
        blk = PostSignal()
        with patch(PostSignal.__module__ + ".WebEngine"):
            with patch(PostSignal.__module__ + ".BuildSignal") as handler:
                self.configure_block(blk, {'include_headers': True})
                handler.assert_called_once_with(
                    blk.endpoint(),
                    ANY,
                    blk.logger,
                    blk.response_headers,
                    blk.include_headers())

    def test_web_handler_post_error(self):
        response_headers = MagicMock()
        handler = BuildSignal(endpoint='',
                              notify_signals=self.notify_signals,
                              logger=MagicMock(),
                              response_headers=response_headers)
        request = MagicMock()
        response = MagicMock()
        request.get_body.return_value = "I'm just a string :("
        handler.on_post(request, response)
        self.assertEqual(response.set_header.call_args_list[0][0][0],
                         'Access-Control-Allow-Origin')
        self.assertEqual(response.set_header.call_args_list[0][0][1],
                         response_headers.return_value.\
                         access_control_allow_origin.return_value)
        self.assertEqual(len(self.last_notified[DEFAULT_TERMINAL]), 0)

    def test_web_handler_options(self):
        response_headers = MagicMock()
        handler = BuildSignal(endpoint='',
                              notify_signals=self.notify_signals,
                              logger=MagicMock(),
                              response_headers=response_headers)
        response = MagicMock()
        handler.on_options(MagicMock(), response)
        self.assertEqual(response.set_header.call_args_list[0][0][0],
                         'Access-Control-Allow-Origin')
        self.assertEqual(response.set_header.call_args_list[0][0][1],
                         response_headers.return_value.\
                         access_control_allow_origin.return_value)
        self.assertEqual(response.set_header.call_args_list[1][0][0],
                         'Access-Control-Allow-Headers')
        self.assertEqual(response.set_header.call_args_list[1][0][1],
                         response_headers.return_value.\
                         access_control_allow_headers.return_value)
        self.assertEqual(len(self.last_notified[DEFAULT_TERMINAL]), 0)
