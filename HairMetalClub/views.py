from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Album
from .serializers import AlbumSerializer
import requests
from django.shortcuts import render
from django.urls import reverse

class AlbumListAPIView(APIView):
    def get(self, request, format=None):
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)
    
def reviews(request):
    api_url = request.build_absolute_uri(reverse('album-list'))
    response = requests.get(api_url)
    albums = response.json()
    return render(request, 'reviews.html', {'albums': albums})

def album_review(request, artist_slug, title_slug):
    api_url = request.build_absolute_uri(reverse('album-list'))
    
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

def reviews_by_tag(request, tag_name):
    api_url = request.build_absolute_uri(reverse('album-list'))


    response = requests.get(api_url)
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.content)

    filtered_albums = response.json()

    return render(request, 'reviews_by_tag.html', {'filtered_albums': filtered_albums})



