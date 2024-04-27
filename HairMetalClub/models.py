from django.db import models
from ckeditor.fields import RichTextField
from colorfield.fields import ColorField
from django.utils.text import slugify

# MOD

class TextBlock(models.Model):
    about_title = models.CharField(max_length=200)
    about_content = RichTextField()
    playlist_title = models.CharField(max_length=200)
    playlist_content = RichTextField()
    contact_title = models.CharField(max_length=200)
    contact_content = RichTextField()

    def __str__(self):
        return "TextBlocks"

class TagGroup(models.Model):
    name = models.CharField(max_length=200)
    color = ColorField(format='hexa', max_length=9)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200)
    tag_group = models.ForeignKey(TagGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Album(models.Model):
    publish_date = models.DateTimeField(auto_now_add=True)
    artist = models.CharField(max_length=200)
    artist_slug = models.SlugField(unique=False)
    title = models.CharField(max_length=200)
    title_slug = models.SlugField(unique=True)
    release_date = models.DateField()
    tracklist = models.TextField()
    image = models.ImageField(upload_to='uploads/album_covers/')
    review = RichTextField()
    highlights = models.TextField(null=True, blank=True)
    lowlights = models.TextField(null=True, blank=True)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 7)], default=1)
    spotify_url = models.URLField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    buy_url = models.URLField(null=True, blank=True)
    average_user_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):
        self.artist_slug = slugify(self.artist)
        self.title_slug = slugify(self.title)
        super(Album, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.artist} - {self.title}, {self.release_date.year}"

    @property
    def average_user_rating(self):
        user_scores = UserScore.objects.filter(album=self)
        if user_scores:
            total_scores = sum(score.score for score in user_scores)
            return total_scores / len(user_scores)
        return None

class UserScore(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 7)])

    def __str__(self):
        return f"{self.album.title} - Score: {self.score}"

