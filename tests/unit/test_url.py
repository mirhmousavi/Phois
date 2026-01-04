from phois import Url


def test_extract_domain_from_url():
    url = "http://wwww.github.com"
    Url(url).domain = "github.com"


def test_extract_suffix_from_url():
    url = "http://wwww.github.com"
    Url(url).suffix = "com"
