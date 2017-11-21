import mock
import unittest
from nambaone.bot import Bot
from unittest.mock import patch, MagicMock
from nambaone.exceptions import ClientException, FileNotFoundException, FileUploadException


class TestBot(unittest.TestCase):
    test_token = 'test_token'

    def setUp(self):
        self.bot = Bot(self.test_token)

    def test_header(self):
        expected_headers = {
            'X-Namba-Auth-Token': 'test_token'
        }

        self.assertEqual(self.bot.header, expected_headers)

    @mock.patch.object(Bot, '_post')
    def test_send_message(self, post_mock):
        chat_id = 1
        content = 'test_content'
        content_type = 'test_content_type'

        self.bot.send_message(chat_id, content, content_type)

        post_mock.assert_called_once_with(
            'https://api.namba1.co/chats/1/write',
            {
                'type': content_type,
                'content': content,
            }
        )

    @mock.patch.object(Bot, '_post')
    def test_create_chat(self, post_mock):
        user_id = 1
        name = 'test_chat_name'
        image = 'test_chat_image'

        chat = self.bot.create_chat(user_id, name, image)

        post_mock.assert_called_once_with(
            'https://api.namba1.co/chats/create',
            {
                'name': name,
                'image': image,
                'members[]': user_id
            }
        )

    @mock.patch.object(Bot, '_get')
    def test_typing_start(self, get_mock):
        self.bot.typing_start(1000)

        get_mock.assert_called_once_with('https://api.namba1.co/chats/1000/typing')

    @mock.patch.object(Bot, '_get')
    def test_typing_stop(self, get_mock):
        self.bot.typing_stop(1000)

        get_mock.assert_called_once_with('https://api.namba1.co/chats/1000/stoptyping')

    @mock.patch('nambaone.bot.requests.get')
    @mock.patch.object(Bot, '_parse_response')
    def test__get(self, parse_response_mock, requests_get_mock):

        self.bot._get('test_url')

        requests_get_mock.assert_called_once_with('test_url', headers=mock.ANY, params=())

    @mock.patch('nambaone.bot.requests.post')
    @mock.patch.object(Bot, '_parse_response')
    def test__post(self, parse_response_mock, requests_post_mock):
        self.bot._post('test_url')

        requests_post_mock.assert_called_once_with('test_url', headers=mock.ANY, data=())

    def test__parse_response_success(self):
        response = MagicMock()
        response.json.return_value = {
            'success': True
        }

        self.bot._parse_response(response)

    def test__parse_response_empty(self):
        method_to_test = self.bot._parse_response

        self.assertRaisesRegex(
            ClientException,
            'No valid response returned',
            method_to_test,
            MagicMock()
        )

    def test__parse_response_error_with_message(self):
        response = MagicMock()
        response.url = 'test_url'

        response.json.return_value = {
            'success': False,
            'message': 'test_error'
        }

        method_to_test = self.bot._parse_response

        self.assertRaisesRegex(
            ClientException,
            'test_error in "test_url" request',
            method_to_test,
            response
        )

    def test__parse_response_error_without_message(self):
        response = MagicMock()
        response.url = 'test_url'

        response.json.return_value = {
            'success': False,
        }

        method_to_test = self.bot._parse_response

        self.assertRaisesRegex(
            ClientException,
            'Unknown error in "test_url" request',
            method_to_test,
            response
        )

    @mock.patch('nambaone.bot.requests.get')
    def test_get_file(self, get_mock):
        m = MagicMock()

        m.content = 'file_content'
        m.json.side_effect = ValueError
        get_mock.return_value = m

        response = self.bot.get_file('file_token')

        get_mock.assert_called_once_with(
            'https://files.namba1.co',
            params={'token': 'file_token'}
        )
        self.assertEqual(response, 'file_content')

    @mock.patch('nambaone.bot.requests.get')
    def test_get_file_error(self, get_mock):
        self.assertRaises(
            ClientException,
            self.bot.get_file,
            'bad_token'
        )

    def test_send_file_no_file(self):
        self.assertRaises(
            FileUploadException,
            self.bot.send_file,
            'file_that_does_not_exist'
        )

    @mock.patch('nambaone.bot.open')
    @mock.patch('nambaone.bot.exists')
    @mock.patch('nambaone.bot.requests.post')
    def test_send_file_error(self, post_mock, exists_mock, open_mock):
        m = MagicMock()
        m.json.return_value = {
            'success': False
        }
        post_mock.return_value = m
        exists_mock.return_value = True
        open_mock.return_value = MagicMock()
        self.assertRaisesRegex(
            FileUploadException,
            'Unknown error',
            self.bot.send_file,
            'file'
        )

    @mock.patch('nambaone.bot.open')
    @mock.patch('nambaone.bot.exists')
    @mock.patch('nambaone.bot.requests.post')
    def test_send_file(self, post_mock, exists_mock, open_mock):
        m = MagicMock()
        m.json.return_value = {
            'success': True,
            'file': 'file_token'
        }
        post_mock.return_value = m
        exists_mock.return_value = True
        open_mock.return_value = MagicMock()

        token = self.bot.send_file('file')
        self.assertEqual(token, 'file_token')
        post_mock.assert_called_once_with(
            'https://files.namba1.co',
            files={'file': mock.ANY}
        )


if __name__ == '__main__':
    unittest.main()
