from django.db import models
from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from account.models import Profile, BaseModel, validate_picture


class Post(BaseModel):
    author = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="posts")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name="posts")
    tags = models.ManyToManyField('Tag', related_name="posts", blank=True)
    pic = models.ImageField(blank=True, null=True, validators=[validate_picture]) 
    text = models.TextField()
    score = models.DecimalField(default=0.0, max_digits=3, decimal_places=1)
    score_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)      
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
    def like(self):
        self.like_count += 1
        self.save()

    def dislike(self):
        self.dislike_count += 1
        self.save()

    def view(self):
        self.view_count += 1
        self.save()

    def calculate_score(self, new_score):
        self.score = (self.score + new_score)/(self.score_count + 1)
        self.score_count += 1
        self.save()

class Category(BaseModel):
    title = models.CharField(max_length=40)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
   
    def __str__(self):  
        return self.title


class Tag(BaseModel):
    title = models.CharField(max_length=40)

    def __str__(self):  
        return self.title


class Comment(BaseModel):
    user   = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post   = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="posts")
    text   = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return "%s  ->  %s" %(self.user, self.post)


class Score(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="scores")
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name="scores")
    value = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)]) 

    def __str__(self):
        return "%s  ->  %s" %(self.user,self.post)
    

class Bookmark(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.PROTECT)
    post = models.ForeignKey(Post, on_delete=models.PROTECT)

    def __str__(self):
        return "%s  ->  %s" %(self.user,self.post)