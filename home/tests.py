from django.contrib.staticfiles.testing import StaticLiveServerTestCase


# Create your tests here.
class ViewTest(StaticLiveServerTestCase):
    def testIndexTemplate(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home/index.html")
