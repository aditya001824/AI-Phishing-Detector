import unittest
from detector import load_artifacts, predict_message


class TestDetector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model, cls.vectorizer = load_artifacts()

    def test_load_artifacts(self):
        self.assertIsNotNone(self.model)
        self.assertIsNotNone(self.vectorizer)

    def test_predict_safe_message(self):
        sample = "Hey, are we still meeting up for lunch today?"
        result = predict_message(sample, self.model, self.vectorizer)

        self.assertEqual(result["result"], "safe")
        self.assertFalse(result["is_phishing"])
        self.assertTrue(0.0 <= result["confidence"] <= 1.0)

    def test_predict_phishing_message(self):
        sample = "URGENT: WINNER! Claim your cash prize instantly by calling now!"
        result = predict_message(sample, self.model, self.vectorizer)

        self.assertEqual(result["result"], "phishing")
        self.assertTrue(result["is_phishing"])
        self.assertTrue(0.0 <= result["confidence"] <= 1.0)

    def test_predict_empty_message(self):
        with self.assertRaises(ValueError):
            predict_message("", self.model, self.vectorizer)

        with self.assertRaises(ValueError):
            predict_message("   ", self.model, self.vectorizer)


if __name__ == "__main__":
    unittest.main()
