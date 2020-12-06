from unittest import TestCase
import requests

from k8_vmware.helpers.for_osbot_utils.Wrap_Method import Wrap_Method


class test_Wrap_Method(TestCase):

    def setUp(self) -> None:
        print()
        self.target        = requests.api.request
        self.target_module = requests.api
        self.target_method = 'request'
        self.wrap_method = Wrap_Method(target_module=self.target_module, target_method=self.target_method)

    def test__init__(self):
        assert self.wrap_method.target        == self.target
        assert self.wrap_method.target_module == self.target_module
        assert self.wrap_method.target_method == self.target_method

    def test___enter__exist(self):
        assert requests.api.request == self.target
        with self.wrap_method:
            assert requests.api.request == self.wrap_method.wrapper_method
            requests.head('https://www.google.com')
            assert self.wrap_method.calls_count() == 1
        assert requests.api.request == self.target

    def test_wrap__unwrap(self):
        assert requests.api.request == self.target

        self.wrapped_method = self.wrap_method.wrap()

        assert requests.api.request != self.target
        assert requests.api.request == self.wrap_method.wrapper_method

        kwargs = { 'method': 'HEAD', 'url':'https://www.google.com'}

        requests.api.request(method='HEAD', url='https://www.google.com')
        requests.api.request(**kwargs)
        requests.head       ('https://www.google.com')
        requests.get        ('https://www.google.com/404')

        assert self.wrap_method.calls_count()            == 4
        assert self.wrap_method.calls[0]['args'        ] == ()
        assert self.wrap_method.calls[0]['kwargs'      ] == {'method': 'HEAD', 'url': 'https://www.google.com'}
        assert self.wrap_method.calls[0]['return_value'].status_code == 200
        assert self.wrap_method.calls[1]['args'        ] == ()
        assert self.wrap_method.calls[1]['kwargs'      ] == {'method': 'HEAD', 'url': 'https://www.google.com'}
        assert self.wrap_method.calls[1]['return_value'].status_code == 200
        assert self.wrap_method.calls[2]['args'        ] == ('head', 'https://www.google.com')
        assert self.wrap_method.calls[2]['kwargs'      ] == {'allow_redirects': False}
        assert self.wrap_method.calls[2]['return_value'].status_code == 200
        assert self.wrap_method.calls[3]['args'        ] == ('get', 'https://www.google.com/404')
        assert self.wrap_method.calls[3]['kwargs'      ] == {'allow_redirects': True, 'params': None}
        assert self.wrap_method.calls[3]['return_value'].status_code == 404

        self.wrap_method.unwrap()

        assert requests.api.request == self.target


    def test_wrap__unwrap___check_original(self):
        assert requests.api.request == self.target
