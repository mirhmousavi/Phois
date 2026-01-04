from phois import Phois


def test_fetch_whois_valid_domain():
    result = Phois().fetch(domain="github.com")
    assert result["registry_result"]
    assert result["registrar_result"]
