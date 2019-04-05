from django.test import TestCase
from .models import Movie
# Create your tests here.

class MovieModelTest(TestCase):
    @classmethod
    def SetUp(cls):
        Movie.objects.create(name='Test Movie', genre='test genre',tmdbId = 1 )

    def test_movie_label(self):
        mov = Movie.objects.get(movie_id=1)
        field_label = mov._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_genre_label(self):
        mov = Movie.objects.get(movie_id=1)
        field_label = mov._meta.get_field('genre').verbose_name
        self.assertEquals(field_label, 'genre')
