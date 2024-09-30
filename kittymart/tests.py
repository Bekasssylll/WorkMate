from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from kittymart.models import Kitten, Rating
from kittymart.serializers import KittenSerializer, UserRegistrationSerializer, RatingSerializer

User = get_user_model()


class KittenSerializerTestCase(APITestCase):
    def setUp(self):
        self.kitten_data = {
            'color': 'Black',
            'age_in_months': 2,
            'description': 'Cute kitten',
            'breed': 'Siamese',
        }
        self.kitten = Kitten.objects.create(**self.kitten_data)

    def test_kitten_serializer(self):
        serializer = KittenSerializer(instance=self.kitten)
        data = serializer.data

        self.assertEqual(data['color'], self.kitten_data['color'])
        self.assertEqual(data['age_in_months'], self.kitten_data['age_in_months'])
        self.assertEqual(data['description'], self.kitten_data['description'])
        self.assertEqual(data['breed'], self.kitten_data['breed'])


class UserRegistrationSerializerTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'testmail@gmail.com',
            'password': 'testpass'
        }

    def test_user_registration_serializer(self):
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))


class RatingSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testmail@gmail.com', password='testpass')
        self.kitten = Kitten.objects.create(color='Black', age_in_months=2, description='Cute kitten', breed='Siamese',
                                            user=self.user)
        self.rating_data = {
            'kitten': self.kitten.id,
            'user': self.user.id,
            'score': 5,
        }

    def test_rating_serializer(self):
        serializer = RatingSerializer(data=self.rating_data)
        self.assertTrue(serializer.is_valid())

        rating = serializer.save()
        self.assertEqual(rating.score, self.rating_data['score'])
        self.assertEqual(rating.kitten.id, self.rating_data['kitten'])
        self.assertEqual(rating.user.username, self.user.username)

    def test_rating_user_read_only(self):
        serializer = RatingSerializer(data=self.rating_data)
        serializer.is_valid()
        self.assertEqual(serializer.validated_data['user'], self.user)



