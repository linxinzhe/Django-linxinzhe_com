from django.test import TestCase


# Create your tests here.
class ViewTest(TestCase):
    def testIndexTemplate(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home/index.html")
