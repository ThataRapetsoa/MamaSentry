"""Structural and domain checks for suspicious URLs."""

from dataclasses import dataclass
from urllib.parse import urlsplit
import ipaddress
import re


@dataclass(frozen=True)
class UrlCheckResult:
    url: str
    valid: bool
    suspicious: bool
    domain: str | None
    reasons: tuple[str, ...]


class UrlChecker:
    """Check URL structure and common phishing indicators without fetching it."""

    def __init__(self, trusted_domains: set[str] | None = None) -> None:
        self.trusted_domains = {domain.casefold() for domain in (trusted_domains or set())}

    def check(self, value: str) -> UrlCheckResult:
        candidate = value.strip()
        parsed = urlsplit(candidate)
        reasons: list[str] = []
        domain = parsed.hostname.casefold() if parsed.hostname else None

        if parsed.scheme not in {"http", "https"} or not domain:
            return UrlCheckResult(candidate, False, True, domain, ("invalid_url",))
        if parsed.username or parsed.password:
            reasons.append("embedded_credentials")
        if parsed.scheme != "https":
            reasons.append("unencrypted_http")
        if self._is_ip_address(domain):
            reasons.append("ip_address_host")
        if domain.startswith("xn--") or ".xn--" in domain:
            reasons.append("internationalized_domain")
        if len(domain.split(".")) > 4:
            reasons.append("deeply_nested_subdomains")
        if re.search(r"(?:login|verify|secure|account|otp|payment)", domain):
            reasons.append("suspicious_domain_keyword")
        if self.trusted_domains and not self._is_trusted(domain):
            reasons.append("untrusted_domain")

        return UrlCheckResult(candidate, True, bool(reasons), domain, tuple(reasons))

    def _is_trusted(self, domain: str) -> bool:
        return any(domain == trusted or domain.endswith(f".{trusted}") for trusted in self.trusted_domains)

    @staticmethod
    def _is_ip_address(domain: str) -> bool:
        try:
            ipaddress.ip_address(domain)
        except ValueError:
            return False
        return True
