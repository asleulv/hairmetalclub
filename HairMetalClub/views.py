from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Album, TextBlock, Tag, TagGroup
from .serializers import AlbumSerializer, TagGroupSerializer, TagSerializer
import requests
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings

class TextBlockAPIView(APIView):
    def get(self, request, format=None):
        textblocks = TextBlock.objects.all()
        serializer = TextBlockSerializer(textblocks, many=True)
        return Response(serializer.data)

class AlbumListAPIView(APIView):
    def get(self, request, format=None):
        albums = Album.objects.all()

        # Calculate the star_rating field for each album
        for album in albums:
            album.star_rating = '★' * album.rating + '☆' * (6 - album.rating)

        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

class TagDataAPIView(APIView):
    def get(self, request, format=None):
        tags = Tag.objects.all()
        tag_groups = TagGroup.objects.all()

        tag_group_serializer = TagGroupSerializer(tag_groups, many=True)
        tag_serializer = TagSerializer(tags, many=True)

        aggregated_data = {
            'tags': tag_serializer.data,
            'tag_groups': tag_group_serializer.data,
        }

        return Response(aggregated_data)

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

    if response.status_code == 200:
        albums = response.json()

        # Filter albums by the specified tag_name
        filtered_albums = [
            album for album in albums
            if any(tag['name'] == tag_name for tag in album.get('tags', []))
        ]

        return render(request, 'reviews_by_tag.html', {'filtered_albums': filtered_albums})
    else:
        # Handle the case when the API request is not successful
        # You might want to display an error message or handle it differently
        return render(request, 'error.html')  # Create an 'error.html' template for displaying errors

def highlights_list(request):
    textblock = TextBlock.objects.values('playlist_title', 'playlist_content').first()
    api_url = request.build_absolute_uri(reverse('album-list'))

    response = requests.get(api_url)
    albums = response.json()

    highlights_data = []

    for album in albums:
        highlights = album.get("highlights", "").split("\r\n")

        for highlight in highlights:
            # Skip empty highlights
            if highlight.strip():
                highlights_data.append({
                    'artist': album.get('artist'),
                    'song_title': highlight.strip(),
                    'title': album.get('title'),
                    'release_date': album.get('release_date'),
                })

    return render(request, 'highlights_list.html', {'highlights_data': highlights_data, 'textblock': textblock})


def tag_list(request):
    api_url = request.build_absolute_uri(reverse('tag-data'))  # Assuming 'tag-data' is the name of your TagDataAPIView URL pattern
    response = requests.get(api_url)
    data = response.json()

    tag_data = data['tags']
    tag_groups = data['tag_groups']

    context = {'tag_data': tag_data, 'tag_groups': tag_groups}
    return render(request, 'tag_list.html', context)

def about(request):
    textblock = TextBlock.objects.values('about_title', 'about_content').first()

    return render(request, 'about.html', {'textblock': textblock})

def contact(request):
    textblock = TextBlock.objects.values('contact_title', 'contact_content').first()
    web3forms_api_key = settings.WEB3FORMS_API_KEY

    return render(request, 'contact.html', {'textblock': textblock, 'web3forms_api_key': web3forms_api_key})




