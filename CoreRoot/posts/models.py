from django.db import models

from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.

from core.models import AbstractModel, AbstractManager


class PostManager(AbstractManager):
    pass


class Post(AbstractModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    edited = models.BooleanField(default=False)
    posts_liked = models.ManyToManyField(User, related_name="post_liked_by" , verbose_name="Post Liked By")
    
    objects = PostManager()

    def like(self, user):
        return self.posts_liked.add(user)
    
    def remove_like(self, user):
        return self.posts_liked.remove(user)
    
    
    def has_liked_by(self, user):
        return self.posts_liked.filter(id=user.id).exists()

    def __str__(self):
        return f"{self.author.name}"
    



class CommentManager(AbstractManager):
    pass


class Comment(AbstractModel):
    post = models.ForeignKey(Post,
                              on_delete=models.PROTECT)
    author = models.ForeignKey(User,
                                on_delete=models.PROTECT)
    body = models.TextField()
    edited = models.BooleanField(default=False)
    objects = CommentManager()
    
    
    def __str__(self):
        return self.author.name