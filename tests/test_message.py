import unittest
from nambaone.message import Message


class TestMessage(unittest.TestCase):

    def test_from_dict(self):

        message_data = {
            'id': 1,
            'type': 'text/plain',
            'content': 'test-content',
            'chat_id': 1000,
        }

        message = Message.from_dict(message_data)

        self.assertEqual(message.id, 1)
        self.assertEqual(message.type, 'text/plain')
        self.assertEqual(message.content, 'test-content')

        self.assertEqual(message.chat.id, 1000)


if __name__ == '__main__':
    unittest.main()
