from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Album
from .serializers import AlbumSerializer
import requests
from django.shortcuts import render

class AlbumListAPIView(APIView):
    def get(self, request, format=None):
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)
    
def reviews(request):
    api_url = 'http://127.0.0.1:8000/api/albums/' 
    response = requests.get(api_url)
    albums = response.json()
    return render(request, 'reviews.html', {'albums': albums})

def album_review(request, artist_slug, title_slug):
    api_url = f'http://127.0.0.1:8000/api/albums/'
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        album_data_list = response.json()

        for album_data in album_data_list:
            if album_data['artist_slug'] == artist_slug and album_data['title_slug'] == title_slug:
                album = album_data
                break
        else:
            album = None
    except requests.exceptions.RequestException as e:
        album = None

    return render(request, 'album_review.html', {'album': album})


