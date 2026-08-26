import unittest
from app import app


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Phishing" in response.data or b"phishing" in response.data.lower())

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertTrue(data["model_loaded"])

    def test_predict_endpoint_safe(self):
        payload = {"message": "Hello, please find the project report attached."}
        response = self.client.post("/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["result"], "safe")
        self.assertFalse(data["is_phishing"])
        self.assertIn("confidence", data)

    def test_predict_endpoint_phishing(self):
        payload = {
            "message": "URGENT: You have won a free prize! Click here to claim immediately: http://claim.fake"
        }
        response = self.client.post("/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["result"], "phishing")
        self.assertTrue(data["is_phishing"])
        self.assertIn("confidence", data)

    def test_predict_endpoint_empty_message(self):
        payload = {"message": "   "}
        response = self.client.post("/predict", json=payload)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_predict_endpoint_missing_payload(self):
        response = self.client.post("/predict", json={})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
