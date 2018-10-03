from unittest import TestCase
from unittest.mock import Mock, patch

import main


def mock_sum(a, b):
    print('Mocked `sum` method')
    return a + b


class TestCalculator(TestCase):
    def test_sum(self):
        answer = main.Calculator().sum(2, 4)
        self.assertEqual(answer, 6)

    @patch('main.Calculator.sum', return_value=6)
    def test_sum_patched(self, sum):
        answer = sum(2, 4)
        self.assertEqual(answer, 6)
        # or
        answer = main.Calculator().sum(2, 4)
        self.assertEqual(answer, 6)

    @patch('main.Calculator.sum', side_effect=mock_sum)
    def test_sum_mocked(self, sum):
        self.assertEqual(sum(2, 3), 5)
        # or
        self.assertEqual(main.Calculator().sum(7, 3), 10)


class TestBlog(TestCase):
    @patch('main.Blog')
    def test_blog_posts(self, MockBlog):
        blog = MockBlog()

        blog.posts.return_value = [
            {
                'userId': 1,
                'id': 1,
                'title': 'Test Title',
                'body': r'Far out in the uncharted backwaters of the unfashionable end of the western spiral arm of the Galaxy\ lies a small unregarded yellow sun.'
            }
        ]

        response = blog.posts()
        self.assertIsNotNone(response)
        self.assertIsInstance(response[0], dict)
        assert MockBlog is main.Blog  # The mock is equivalent to the original
        assert MockBlog.called  # The mock was called
        blog.posts.assert_called_with()  # We called the posts method with no arguments
        # We called the posts method once with no arguments
        blog.posts.assert_called_once_with()
        # blog.posts.assert_called_with(1, 2, 3) - This assertion is False and
        # will fail since we called blog.posts with no arguments
        blog.reset_mock()  # Reset the mock object
        # After resetting, posts has not been called.
        blog.posts.assert_not_called()
