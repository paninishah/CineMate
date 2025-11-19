from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
import json

from .models import Movie, Rating

@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8")) #convert whatever postman says which is in json to python dict

        username = data.get("username")
        password = data.get("password")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "User already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user) #,- ignore the second value returned 

        return JsonResponse({"username": user.username, "token": token.key})

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({"username": username, "token": token.key})


@csrf_exempt
def logout_view(request):
    if request.method == "POST":
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Token "):
            return JsonResponse({"error": "Token missing"}, status=400)

        token_key = auth_header.split(" ")[1]
        Token.objects.filter(key=token_key).delete()

        return JsonResponse({"message": "Logged out"})

@csrf_exempt
def add_movie(request):
    if request.method == "POST":
        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Token "):
            return JsonResponse({"error": "Authentication required"}, status=403)

        token = auth.split(" ")[1]

        try:
            user = Token.objects.get(key=token).user
        except:
            return JsonResponse({"error": "Invalid token"}, status=400)

        data = json.loads(request.body.decode("utf-8"))

        movie = Movie.objects.create(
            title=data.get("title"),
            year=data.get("year"),
            genre=data.get("genre"),
            duration=data.get("duration"),
            synopsis=data.get("synopsis"),
            user=user
        )

        return JsonResponse({"message": "Movie added", "movie_id": movie.movie_id})


@csrf_exempt
def get_movies(request):
    movies = Movie.objects.all()
    output = []

    for m in movies:
        output.append({
            "movie_id": m.movie_id,
            "title": m.title,
            "year": m.year,
            "genre": m.genre,
            "duration": m.duration,
            "synopsis": m.synopsis,
            "added_by": m.user.username,
            "created_at": str(m.created_at)
        })

    return JsonResponse(output, safe=False)

@csrf_exempt
def delete_movie(request, movie_id):
    if request.method == "POST":
        movie = Movie.objects.filter(movie_id=movie_id).first()

        if movie is None:
            return JsonResponse({"error": "Movie not found"}, status=404)

        movie.delete()

        return JsonResponse({"message": "Movie deleted"})

@csrf_exempt
def rate_movie(request):
    if request.method == "POST":
        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Token "):
            return JsonResponse({"error": "Authentication required"}, status=403)

        token = auth.split(" ")[1]

        user = Token.objects.get(key=token).user

        data = json.loads(request.body.decode("utf-8"))

        movie_id = data.get("movie_id")
        rating_val = data.get("rating_value")

        movie = Movie.objects.filter(movie_id=movie_id).first()

        if movie is None:
            return JsonResponse({"error": "Movie not found"}, status=404)

        Rating.objects.create(
            user=user,
            movie=movie,
            rating_value=rating_val
        )

        return JsonResponse({"message": "Rating added"})

