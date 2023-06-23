from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .serializers import FilmworkSerializer
from movies.models import Filmwork, Genre, GenreFilmwork


class MoviesViewSet(viewsets.ModelViewSet):

    queryset = Filmwork.objects.prefetch_related('genres').all()
    serializer_class = FilmworkSerializer
    http_method_names = ['get', ]
