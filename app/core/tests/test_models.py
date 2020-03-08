from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        email='12vfs'
        password='ZAdabc123'

        user=get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):

        email="dse@GMail.com"

        user = get_user_model().objects.create_user(email=email, password= "vfff")

        self.assertEqual(user.email, email.lower())


    def test_create_new_superuser(self):

        email='mai@gmail.com'

        password='abc123'

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_staff)

        self.assertTrue(user.is_superuser)
