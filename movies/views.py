from django.shortcuts import render
from .models import Movie
from django.shortcuts import render, get_object_or_404

def xemphim(request,slug):
    movie = get_object_or_404(Movie, slug=slug)
    movies = Movie.objects.all()
    context = {
        'movies': movies,
        'movie':movie
    }
    return render(request, 'xemphim.html',context)