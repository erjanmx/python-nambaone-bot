import mock
import unittest
from nambaone.bot import Bot
from unittest.mock import MagicMock


class TestBot(unittest.TestCase):
    test_token = 'test_token'

    def setUp(self):
        self.bot = Bot(self.test_token)

    def test_header(self):
        expected_headers = {
            'X-Namba-Auth-Token': 'test_token'
        }

        self.assertEqual(self.bot.header, expected_headers)

    @mock.patch('nambaone.bot.requests.post')
    def test_send_message(self, requests_post_mock):
        chat_id = 1
        content = 'test_content'
        content_type = 'test_content_type'

        requests_post_json_mock = MagicMock()
        requests_post_json_mock.json.return_value = {
            'data': {
                'id': 1000,
                'type': content_type,
                'content': content,
                'chat_id': chat_id,
            },
        }

        requests_post_mock.return_value = requests_post_json_mock

        message = self.bot.send_message(chat_id, content, content_type)

        requests_post_mock.assert_called_once_with(
            'https://api.namba1.co/chats/1/write',
            {
                'type': content_type,
                'content': content,
            },
            headers=mock.ANY
        )

        self.assertEqual(message.id, 1000)

    @mock.patch('nambaone.bot.requests.post')
    def test_create_chat(self, requests_post_mock):
        user_id = 1
        name = 'test_chat_name'
        image = 'test_chat_image'

        requests_post_json_mock = MagicMock()
        requests_post_json_mock.json.return_value = {
            'data': {
                'id': 1000,
                'name': name,
                'image': image,
            },
        }

        requests_post_mock.return_value = requests_post_json_mock

        chat = self.bot.create_chat(user_id, name, image)

        requests_post_mock.assert_called_once_with(
            'https://api.namba1.co/chats/create',
            {
                'name': name,
                'image': image,
                'members[]': user_id
            },
            headers=mock.ANY
        )

        self.assertEqual(chat.id, 1000)

    @mock.patch('nambaone.bot.requests.get')
    def test_typing_start(self, requests_get_mock):
        self.bot.typing_start(1000)

        requests_get_mock.assert_called_once_with(
            'https://api.namba1.co/chats/1000/typing',
            headers=mock.ANY
        )

    @mock.patch('nambaone.bot.requests.get')
    def test_typing_stop(self, requests_get_mock):
        self.bot.typing_stop(1000)

        requests_get_mock.assert_called_once_with(
            'https://api.namba1.co/chats/1000/stoptyping',
            headers=mock.ANY
        )


if __name__ == '__main__':
    unittest.main()
