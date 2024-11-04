#!/usr/bin/env python3
'''first task'''
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from typing import Any, Tuple, Dict
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    '''testing uutils'''

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(
        self, n_map: Dict[str, Any], p: Tuple[str], exp: Any
    ) -> None:
        '''testing uutils'''
        self.assertEqual(access_nested_map(n_map, p), exp)

    @parameterized.expand([({}, ("a",)), ({"a": 1}, ("a", "b"))])
    def test_access_nested_map_exception(
        self, n_map: Dict[str, Any], p: Tuple[str]
    ) -> None:
        '''testing uutils'''
        with self.assertRaises(KeyError):
            access_nested_map(n_map, p)


class TestGetJson(unittest.TestCase):
    '''testing uutils'''

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("requests.get")
    def test_get_json(
        self, url: str, payload: Dict[str, Any], mock_get: Mock
    ) -> None:
        '''testing uutils'''
        mock_get.return_value.json.return_value = payload
        self.assertEqual(get_json(url), payload)
        mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    '''testing uutils'''

    def test_memoize(self) -> None:
        '''testing uutils'''

        class TestCls:
            '''testing uutils'''

            def a_mthd(self) -> int:
                '''testing uutils'''
                return 42

            @memoize
            def a_prop(self) -> int:
                '''testing uutils'''
                return self.a_mthd()

        with patch.object(TestCls, "a_mthd", return_value=42) as mock:
            t_cls = TestCls()
            self.assertEqual(t_cls.a_prop, 42)
            self.assertEqual(t_cls.a_prop, 42)
            mock.assert_called_once()
