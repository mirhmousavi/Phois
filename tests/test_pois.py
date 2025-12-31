import time

import pytest
import json
from phois import Phois, NoWhoisServerFoundError


class TestPhois:
    def test_phois_result_have_both_registry_and_registrar_keys(self):
        result = Phois().fetch(domain="github.com")
        assert "registry_result" in result
        assert "registrar_result" in result

    def test_fetch_whois_of_valid_domain(self):
        result = Phois().fetch(domain="github.com")
        assert result

    @pytest.mark.skip
    def test_fetch_whois_of_valid_domain_with_not_utf8_result(self):
        result = Phois().fetch(domain="cloudpbx.com.tr")["registry_result"]
        assert result

    def test_fetch_whois_of_idn(self):
        result = Phois().fetch(domain="购物.购物")["registry_result"]
        assert result

    @pytest.mark.skip
    def test_fetch_whois_of_valid_domain_with_proxy(self):
        result = Phois(
            proxy_info={"type": "http", "addr": "localhost", "port": 8118}
        ).fetch(domain="github.com")["registry_result"]
        assert result

    def test_fetch_whois_of_valid_domain_with_defined_whois_server(self):
        result = Phois().fetch(
            domain="github.com", whois_server="whois.verisign-grs.com"
        )["registry_result"]
        assert result

    def test_fetch_whois_of_not_exist_domain(self):
        result = Phois().fetch(domain="notexistdomain123.com")["registry_result"]
        assert result

    def test_fetch_whois_of_not_exists_tld(self):
        with pytest.raises(NoWhoisServerFoundError):
            Phois().fetch(domain="github.az")

    def test_update_tld_file(self):
        random = int(time.time())
        p = Phois()
        p.update_tlds_file({"random": random})
        with open(Phois.tlds_file_path, "r") as f:
            content = json.load(f)
            assert content["random"] == random

    def test_find_whois_server_for_tld(self):
        result = Phois().find_whois_server_for_tld("guru")
        assert result == "whois.nic.guru"

    def test_find_whois_server_for_not_exists_tld(self):
        with pytest.raises(NoWhoisServerFoundError):
            Phois().find_whois_server_for_tld("xxxxxxxxxxxxx123")

    # def test_get_idna_repr_non_ascii_input(self):
    #     p = Phois()
    #     result = p.get_idna_repr('سلام')
    #     expected_result = 'xn--mgbx5cf'
    #     assert result == expected_result
    #
    # def test_get_idna_repr_ascii_input(self):
    #     p = Phois()
    #     result = p.get_idna_repr('hello')
    #     expected_result = 'hello'
    #     assert result == expected_result
