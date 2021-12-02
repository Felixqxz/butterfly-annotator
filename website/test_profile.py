import unittest
from flask import Flask
# from fastapi.testclient import TestClient
from app import app
# from flask import current_app
# client = TestClient(app)

class ProfileTestCase(unittest.TestCase):

    def test_get_user_profile_successful(self):
        tester = app.test_client(self)
        response = tester.get("/base-data")
        assert response.status_code == 200
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
  unittest.main()

# Integration test to be added for groups after we complete all group functionality
