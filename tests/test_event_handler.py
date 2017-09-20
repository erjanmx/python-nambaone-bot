import mock
import unittest
from src.bot import Bot
from src.user import User
from src.update import Update
from unittest.mock import MagicMock
from src.event_handler import EventHandler


class TestEventHandler(unittest.TestCase):
    success_response = {
        'code': 200,
        'success': True,
    }

    def setUp(self):
        self.bot = Bot('test_token')
        self.handler_mock = MagicMock()

    def test_run_user_follow(self):
        self.bot.handler.add('user_follow', self.handler_mock)

        self.bot.run({
            'event': 'user/follow',
            'data': {
                'id': 1,
                'name': 'test-name',
                'gender': 'M',
            }
        })

        self.handler_mock.assert_called_once_with(self.bot, mock.ANY)

        self.assertEqual(self.bot.response, self.success_response)


    def test_run_user_unfollow(self):
        self.bot.handler.add('user_unfollow', self.handler_mock)

        self.bot.run({
            'event': 'user/unfollow',
            'data': {
                'id': 1,
            }
        })

        self.handler_mock.assert_called_once_with(self.bot, mock.ANY)

        self.assertEqual(self.bot.response, self.success_response)

    def test_run_message_new(self):
        self.bot.handler.add('message_new', self.handler_mock)

        self.bot.run({
            'event': 'message_new',
            'data': {
                'sender_id': 1,
                'chat_id': 10,

                'id': 100,
                'type': 'text/plain',
                'status': 0,
                'content': 'test-content',
            }
        })

        self.handler_mock.assert_called_once_with(self.bot, mock.ANY)

        self.assertEqual(self.bot.response, self.success_response)

    def test_run_chat_new(self):
        self.bot.handler.add('chat_new', self.handler_mock)

        self.bot.run({
            'event': 'chat_new',
            'data': {
                'id': 100,
                'user': {
                    'id': 1,
                    'name': 'test-name',
                    'gender': 'M',
                }
            }
        })

        self.handler_mock.assert_called_once_with(self.bot, mock.ANY)

        self.assertEqual(self.bot.response, self.success_response)


    def test_run_message_update(self):
        self.bot.handler.add('message_update', self.handler_mock)

        self.bot.run({
            'event': 'message_update',
            'data': {
                'sender_id': 1,
                'chat_id': 10,

                'id': 100,
                'type': 'text/plain',
                'status': 1,
                'content': 'test-content',
            }
        })

        self.handler_mock.assert_called_once_with(self.bot, mock.ANY)

        self.assertEqual(self.bot.response, self.success_response)


if __name__ == '__main__':
    unittest.main()
