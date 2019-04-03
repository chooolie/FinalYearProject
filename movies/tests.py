from django.test import TestCase
from .models import Movie
# Create your tests here.

class MovieModelTest(TestCase):
    @classmethod
    def SetUp(cls):
        Movie.objects.create(name='Test Movie', genre='test genre')
