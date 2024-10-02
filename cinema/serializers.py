from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, IntegerField
from rest_framework.relations import SlugRelatedField

from cinema.models import (
    Genre,
    Actor,
    Movie,
    CinemaHall,
    MovieSession,
    Order,
    Ticket
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")
        read_only_fields = ["id"]


class ActorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="__str__", read_only=True)

    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")
        read_only_fields = ["id"]


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "description",
            "duration",
            "genres",
            "actors"
        )
        read_only_fields = ["id"]


class MovieListSerializer(serializers.ModelSerializer):
    genres = SerializerMethodField()
    actors = SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "description",
            "duration",
            "genres",
            "actors"
        )
        read_only_fields = ["id"]

    def get_genres(self, obj):
        return [genre.name for genre in obj.genres.all()]

    def get_actors(self, obj):
        return [str(actor) for actor in obj.actors.all()]


class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")
        read_only_fields = ["id", "capacity"]


class MovieSessionSerializer(serializers.ModelSerializer):
    movie_title = SerializerMethodField()
    cinema_hall_name = SerializerMethodField()

    class Meta:
        model = MovieSession
        fields = ('id', 'show_time', 'movie_title', 'cinema_hall_name')
        read_only_fields = ['id']

    def get_movie_title(self, obj):
        return obj.movie.title if obj.movie else None

    def get_cinema_hall_name(self, obj):
        return obj.cinema_hall.name if obj.cinema_hall else None

    class Meta:
        model = MovieSession
        fields = ("id", "show_time", "movie", "cinema_hall")
        read_only_fields = ["id"]


class MovieSessionListSerializer(serializers.ModelSerializer):
    movie_title = SerializerMethodField()
    cinema_hall_name = SerializerMethodField()
    cinema_hall_capacity = SerializerMethodField()

    def get_movie_title(self, obj):
        return obj.movie.title if obj.movie else None

    def get_cinema_hall_name(self, obj):
        return obj.cinema_hall.name if obj.cinema_hall else None

    def get_cinema_hall_capacity(self, obj):
        return obj.cinema_hall.capacity if obj.cinema_hall else None

    class Meta:
        model = MovieSession
        fields = (
            "id",
            "show_time",
            "movie_title",
            "cinema_hall_name",
            "cinema_hall_capacity",
        )




class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "created_at", "user")
        read_only_fields = ["id", "created_at"]


class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "movie_session", "order", "row", "seat")
        read_only_fields = ["id"]