import unittest
from unittest.mock import MagicMock, Mock, create_autospec, patch

import main


class TestCase(unittest.TestCase):

    def test_mock(self):
        thing = MagicMock(return_value=3)
        result = thing(3, 4, 5, key='value')
        thing.assert_called_with(3, 4, 5, key='value')
        self.assertEqual(result, 3)

    def test_side_effect_1(self):
        mock = Mock(side_effect=KeyError('foo'))
        with self.assertRaises(KeyError):
            mock()

    def test_side_effect_2(self):
        # Side effect as function
        def side_effect(arg):
            values = {'a': 1, 'b': 2, 'c': 3}
            return values[arg]

        mock = Mock()
        mock.side_effect = side_effect
        self.assertEqual(mock('c'), 3)
        self.assertEqual(mock('b'), 2)
        self.assertEqual(mock('a'), 1)

        # Side effect as list
        mock.side_effect = [100, 200]
        self.assertEqual(mock(), 100)
        self.assertEqual(mock(), 200)

    def test_patch_1(self):
        with patch.object(main.Production, 'deploy', return_value=False):
            thing = main.Production()
            self.assertFalse(thing.deploy())

        # Outside patch scope
        thing = main.Production()
        self.assertTrue(thing.deploy())

    def test_magic_methods(self):
        # Magic mock
        magic_mock = MagicMock()
        magic_mock.__str__.return_value = 'foobarbaz'
        str_result = str(magic_mock)
        self.assertEqual(str_result, 'foobarbaz')
        magic_mock.__str__.assert_called()

        # Mock can't be used for magic methods.
        with self.assertRaises(AttributeError):
            mock = Mock()
            mock.__str__.return_value = 'foobarbaz'

        # In case it's needed - magic methods must be mocked first.
        mock = Mock()
        mock.__str__ = Mock(return_value='wheeeeee')
        str_result = str(mock)
        self.assertEqual(str_result, 'wheeeeee')
        magic_mock.__str__.assert_called()

    def test_create_autospec(self):
        production_mock = create_autospec(main.Production)

        with self.assertRaises(TypeError):
            production_mock.deploy('unexpected argument')
        
        production_mock.deploy()
        production_mock.deploy.assert_called()
