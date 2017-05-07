from django.contrib.auth.models import User
from django.test import TestCase


class ChatsViewsTestCase(TestCase):
    """
    This test case checks if a logged in user can access inbox and if inbox view context
    contains these keys: user list and logged in user information
    """
    fixtures = ['chats_data.json']

    def setUp(self):
        user = User.objects.create_user(username='sara', password='123')
        self.client.login(username='sara', password='123')

    def test_inbox(self):
        resp = self.client.get('/chats/inbox/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('userList' in resp.context)
        self.assertTrue('activeUserName' in resp.context)
        self.assertTrue('activeUserId' in resp.context)

