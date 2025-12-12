from django.db import models
from django.contrib.auth.models import User
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

# Helper function for transliteration
def transliterate_to_hindi(text):
    if text:
        try:
            return transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)
        except:
            return text
    return text


# ----------------------
# Category Model
# ----------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def save(self, *args, **kwargs):
        # Transliterate category name to Hindi
        self.name = transliterate_to_hindi(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


# ----------------------
# Reporter Model
# ----------------------
class Reporter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='reporters/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Transliterate reporter bio to Hindi
        self.bio = transliterate_to_hindi(self.bio)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


# ----------------------
# Article Model
# ----------------------
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    reporter = models.ForeignKey(Reporter, on_delete=models.SET_NULL, null=True, blank=True)
    rank = models.IntegerField(default=0)
    
    # Featured media
    
    published_date = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Transliterate title and content to Hindi
        self.title = transliterate_to_hindi(self.title)
        self.content = transliterate_to_hindi(self.content)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


# ----------------------
# Multiple Additional Images
# ----------------------
class ArticleImage(models.Model):
    article = models.ForeignKey(Article, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='article_images/')

    def __str__(self):
        return f'Image for {self.article.title}'


# ----------------------
# Multiple Additional Videos
# ----------------------
class ArticleVideo(models.Model):
    article = models.ForeignKey(Article, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='article_videos/')

    def __str__(self):
        return f'Video for {self.article.title}'


# ----------------------
# Comments for Article
# ----------------------
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)  # name of the user who commented
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def save(self, *args, **kwargs):
        # Transliterate comment body and author name to Hindi
        self.author_name = transliterate_to_hindi(self.author_name)
        self.body = transliterate_to_hindi(self.body)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Comment by {self.author_name} on {self.article.title}'
