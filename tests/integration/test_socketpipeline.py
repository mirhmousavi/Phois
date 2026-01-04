import pytest

from phois import SocketPipeline, SocketError, SocketTimeoutError


def test_execute_whois_with_valid_whois_server():
    result = SocketPipeline().execute(
        query="github.com\r\n", server="whois.verisign-grs.com", port=43
    )
    assert result


def test_execute_whois_with_bad_whois_server():
    with pytest.raises(SocketError):
        SocketPipeline().execute(
            query="github.com\r\n", server="7465.whois-servers.net", port=43
        )


def test_execute_whois_with_bad_domain():
    with pytest.raises(SocketError):
        SocketPipeline().execute(
            query="github\r\n", server="7465.whois-servers.net", port=43
        )


def test_whois_with_low_timeout_that_raises_timeout_error():
    with pytest.raises(SocketTimeoutError):
        SocketPipeline(timeout=1).execute(
            query="github.com", server="whois.verisign-grs.com", port=43
        )
