from app.services.url_checker import UrlChecker


def test_url_checker_flags_untrusted_http_url() -> None:
    result = UrlChecker({"fnb.co.za"}).check("http://secure-login.example.com/verify")

    assert result.valid is True
    assert result.suspicious is True
    assert "unencrypted_http" in result.reasons
    assert "untrusted_domain" in result.reasons


def test_url_checker_accepts_trusted_subdomain() -> None:
    result = UrlChecker({"fnb.co.za"}).check("https://online.fnb.co.za/account")

    assert result.valid is True
    assert result.suspicious is False
    assert result.domain == "online.fnb.co.za"


def test_url_checker_rejects_missing_scheme() -> None:
    result = UrlChecker().check("example.com/login")

    assert result.valid is False
    assert result.reasons == ("invalid_url",)
