import unittest
from heuristics import extract_urls, analyze_urls, analyze_heuristics


class TestHeuristics(unittest.TestCase):
    def test_extract_urls_empty(self):
        self.assertEqual(extract_urls("Hello world with no links"), [])

    def test_extract_urls_various_protocols(self):
        text = "Visit https://google.com and http://example.org/test?id=1 or www.sub.domain.co"
        urls = extract_urls(text)
        self.assertTrue(len(urls) >= 2)

    def test_analyze_urls_ip_address(self):
        urls = ["http://192.168.1.100/login"]
        data = analyze_urls(urls)
        self.assertTrue(data["has_ip_address_url"])

    def test_analyze_urls_shortener(self):
        urls = ["https://bit.ly/3xSample"]
        data = analyze_urls(urls)
        self.assertTrue(data["has_shortened_url"])

    def test_analyze_urls_suspicious_tld(self):
        urls = ["https://free-gifts.xyz/claim"]
        data = analyze_urls(urls)
        self.assertIn(".xyz", data["suspicious_tlds"])

    def test_analyze_heuristics_high_risk(self):
        sample = (
            "URGENT: Your account suspended! Immediate action required to verify your password reset. "
            "Click http://192.168.1.1/reset or win lottery prize $$$!"
        )
        res = analyze_heuristics(sample)
        self.assertEqual(res["risk_level"], "HIGH")
        self.assertGreaterEqual(res["heuristic_score"], 60)
        self.assertGreater(len(res["flags"]), 0)

    def test_analyze_heuristics_safe(self):
        sample = "Hi John, let's schedule our quarterly review for next Tuesday at 3pm."
        res = analyze_heuristics(sample)
        self.assertEqual(res["risk_level"], "LOW")
        self.assertEqual(len(res["flags"]), 0)


if __name__ == "__main__":
    unittest.main()
