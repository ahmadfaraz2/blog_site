from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish'] # show posts from oldest to newest
        indexes = [
            models.Index(fields=['-publish'])  #Improve preformance for queries filtering or ordering results by this field(publish).
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])
    


# Canonical Urls:
#  acha hum ny yeh get_absolute_url() method define kya hai 
#  reverse function ko use kr k "post_detail" k liy.
#  Advantage:
#          Is ka faida yeh ho ga na k har jaga template main {% url 'blog:post_detail' post.id %}
#          likny ki bajay mai uder get_absolute_url() likh dun ga. aur wo apny ap ayk url mai change
#          ho jay ga.
#          Acha yeh args=[] parameters hain basically jo hum view function mai use karty hian.
# Question:
#           Humy kasy pata chalta hai k url is view k liy hai?
# Answer: 
#          Basically reverse main hum jo "app" name aur "url" name use kr rhy hoty hain.



# What really unique_for_date('publish') says?
# unique_for_date('publish') yeh kahti hai k is date('publish') ko slug ayk(single) hi honi chai. 





class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]


    def __str__(self):
        return f"Comment by {self.name} on {self.post}"    
    


# ---------------->>>>related_name<<<<---------------------

# What is the purpose of related_name?
#   The purpose of 'related_name' is to provide a way to access related object("Comment" model) 
#   from the other end of relation('Post' model). 
# 
#   In this case, it allows us to access comments related to a post using the comments attribute
#   of a Post instance.
#   For example, if post is an instance of Post, we can access its comments using
#   post.comments.all().
