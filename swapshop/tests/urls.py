from django.test import TestCase

# Create your tests here.
class URLTests(TestCase):
    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)

    def test_contact(self):
        response = self.client.get("/contact-us/")
        self.assertEqual(response.status_code, 200)

    def test_social(self):
        response = self.client.get("/social/")
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get("/accounts/logout/")
        self.assertEqual(response.status_code, 302)

    def test_profile(self):
        response = self.client.get("/accounts/profile/")
        self.assertEqual(response.status_code, 302)

    def test_search(self):
        response = self.client.get("/search/?keyword=test")
        self.assertEqual(response.status_code, 200)

    def test_social(self):
        response = self.client.get("/all-items/")
        self.assertEqual(response.status_code, 200)

    def test_social(self):
        response = self.client.get("/add/")
        self.assertEqual(response.status_code, 200)
