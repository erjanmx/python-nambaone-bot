import unittest
from src.chat import Chat


class TestChat(unittest.TestCase):

    def test_from_dict(self):
        chat_data = {
            'id': 1,
            'name': 'test-name',
            'image': 'test-image',
        }

        chat = Chat.from_dict(chat_data)

        self.assertEqual(chat.id, 1)
        self.assertEqual(chat.name, 'test-name')
        self.assertEqual(chat.image, 'test-image')


if __name__ == '__main__':
    unittest.main()
