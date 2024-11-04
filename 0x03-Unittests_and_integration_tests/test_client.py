#!/usr/bin/env python3
'''testing test jgnkjsd'''
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import unittest
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    '''later later later'''

    @parameterized.expand(
        [
            ("google"),
            ("abc"),
        ]
    )
    @patch("client.get_json", return_value={"payload": True})
    def test_org(self, org: str, mock_get: Mock) -> None:
        '''later later later'''
        client = GithubOrgClient(org)
        self.assertEqual(client.org, {"payload": True})
        url = f"https://api.github.com/orgs/{org}"
        mock_get.assert_called_once_with(url)

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org) -> None:
        '''later later later'''
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        mock_org.return_value = payload
        client = GithubOrgClient("google")
        self.assertEqual(client._public_repos_url, payload["repos_url"])

    @patch("client.get_json",
           return_value=[{"name": "repo1"}, {"name": "repo2"}])
    def test_public_repos(self, mock_get_json) -> None:
        '''later later later'''
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = (
                "https://api.github.com/orgs/google/repos"
            )
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_json.assert_called_once()
            mock_repos_url.assert_called_once()

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, lic_key, exp_res) -> None:
        '''later later later'''
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, lic_key), exp_res)


@parameterized_class(('org_pl', 'repos_pl', 'exp_repos', 'apache_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    '''later later later'''
    @classmethod
    def setUpClass(cls):
        '''later later later'''
        cls.get_patch = patch("requests.get")
        cls.mock_get = cls.get_patch.start()

        def side_effect(url):
            '''later later later'''
            class MockResponse:
                def __init__(self, json_data):
                    self.json_data = json_data

                def json(self):
                    return self.json_data

            if url.endswith("/orgs/google"):
                return MockResponse(cls.org_pl)
            elif url.endswith("/orgs/google/repos"):
                return MockResponse(cls.repos_pl)
            else:
                return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        '''later later later'''
        cls.get_patch.stop()

    def test_public_repos(self):
        '''later later later'''
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.exp_repos)

    def test_public_repos_with_license(self):
        '''later later later'''
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache_repos)
