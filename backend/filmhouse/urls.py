from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('get_movies/', views.get_movies, name='get_movies'),
    path('delete_movie/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('rate_movie/', views.rate_movie, name='rate_movie'),
]

