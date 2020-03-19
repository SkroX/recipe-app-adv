from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='abc@gmail.com', password='abc123'):

    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        email = '12vfs'
        password = 'ZAdabc123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):

        email = "dse@GMail.com"

        user = get_user_model().objects.create_user(email=email, password="vfff")

        self.assertEqual(user.email, email.lower())

    def test_create_new_superuser(self):

        email = 'mai@gmail.com'

        password = 'abc123'

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_staff)

        self.assertTrue(user.is_superuser)

    def test_tag_str(self):

        tag = models.Tag.objects.create(
            user=sample_user(),
            name='vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):

        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='cucumber'
        )

        self.assertTrue(str(ingredient), ingredient.name)

    def test_recipe_str(self):

        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='mushroom sauce',
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)
