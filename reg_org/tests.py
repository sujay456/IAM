from django.test import TestCase

from reg_org.models import Permissions,Organization
from django.contrib.auth.models import User

# Create your tests here.

class ModelTesting(TestCase):

    def setUp(self):
        self.user=User.objects.create(username="test")
        self.user.set_password("test")
        self.user.save()
        
        self.org=Organization(org_name="test",head_user=self.user)

        self.permission=Permissions(org=self.org,permission_name="test")
    def test_user_model(self):
        d=self.user

        self.assertTrue(isinstance(d,User))

    def test_organization_model(self):
        d=self.org
        self.assertTrue(isinstance(d,Organization))

        self.assertEqual(str(d),"test - test")

    def test_permission_model(self):
        d=self.permission
        self.assertTrue(isinstance(d,Permissions))
        self.assertEqual("test",str(d))
