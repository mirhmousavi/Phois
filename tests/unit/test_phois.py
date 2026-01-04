import time

import pytest
import json
from phois import Phois, NoWhoisServerFoundError
from unittest.mock import patch

from phois.errors import BadDomainError


@patch("phois.SocketPipeline")
def test_fetch_whois_of_valid_domain(mock_socket_pipeline_class):
    ret = []
    for i in ("registry", "registrar"):
        with open(f"tests/artifacts/github.com_{i}.txt", "r") as f:
            ret += [f.read()]

    mock_socket_pipeline_class.return_value.execute.side_effect = ret

    result = Phois().fetch(domain="github.com")
    assert result["registry_result"]
    assert result["registrar_result"]


@patch("phois.SocketPipeline")
def test_fetch_whois_of_valid_domain_with_non_utf8_result(mock_socket_pipeline_class):
    with open("tests/artifacts/non_utf8.txt", "r", encoding="ISO-8859-9") as f:
        mock_socket_pipeline_class.return_value.execute.return_value = f.read()

    result = Phois().fetch(domain="hm.com.tr")["registry_result"]
    assert result


@patch("phois.SocketPipeline")
def test_fetch_whois_idn_domain(mock_socket_pipeline_class):
    with open("tests/artifacts/idn.txt", "r") as f:
        mock_socket_pipeline_class.return_value.execute.return_value = f.read()

    result = Phois().fetch(domain="购物.购物")["registry_result"]
    assert result


@patch("phois.SocketPipeline")
def test_fetch_whois_valid_domain_with_proxy(mock_socket_pipeline_class):
    with open(
        "tests/artifacts/github.com_registry.txt", "r", encoding="ISO-8859-9"
    ) as f:
        mock_socket_pipeline_class.return_value.execute.return_value = f.read()

    result = Phois(
        proxy_info={"type": "http", "addr": "localhost", "port": 8118}
    ).fetch(domain="github.com")["registry_result"]
    assert result


@patch("phois.SocketPipeline")
def test_fetch_whois_valid_domain_with_defined_whois_server(
    mock_socket_pipeline_class,
):
    with open(
        "tests/artifacts/github.com_registry.txt", "r", encoding="ISO-8859-9"
    ) as f:
        mock_socket_pipeline_class.return_value.execute.return_value = f.read()

    result = Phois().fetch(domain="github.com", whois_server="whois.verisign-grs.com")[
        "registry_result"
    ]
    assert result
    mock_socket_pipeline_class.return_value.execute.assert_any_call(
        query="github.com\r\n", server="whois.verisign-grs.com", port=43
    )


@patch("phois.SocketPipeline")
def test_fetch_whois_invalid_domain(mock_socket_pipeline_class):
    with open("tests/artifacts/invalid_domain.txt", "r") as f:
        mock_socket_pipeline_class.return_value.execute.return_value = f.read()

    result = Phois().fetch(domain="notexistdomain123.com")["registry_result"]
    assert result


def test_fetch_whois_of_not_exists_tld():
    with pytest.raises(BadDomainError):
        Phois().fetch(domain="github.gggggg")


def test_update_tld_file():
    random = int(time.time())
    p = Phois()
    p.update_tlds_file({"random": random})
    with open(Phois.tlds_file_path, "r") as f:
        content = json.load(f)
        assert content["random"] == random


@patch("phois.SocketPipeline")
def test_find_whois_server_for_tld(mock_socket_pipeline_class):
    with open("tests/artifacts/tld_guru.txt", "r") as f:
        mock_socket_pipeline_class.return_value.execute.return_value = f.read()

    result = Phois().find_whois_server_for_tld("guru")
    assert result == "whois.nic.guru"


@patch("phois.SocketPipeline")
def test_find_whois_server_for_not_exists_tld(mock_socket_pipeline_class):
    with open("tests/artifacts/invalid_tld.txt", "r") as f:
        mock_socket_pipeline_class.return_value.execute.return_value = f.read()

    with pytest.raises(NoWhoisServerFoundError):
        Phois().find_whois_server_for_tld("gggggg")
