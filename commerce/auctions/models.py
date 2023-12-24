from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryType = models.CharField(max_length=64)

    def __str__(self):
        return self.categoryType
    
class Bid(models.Model):
    bid = models.DecimalField(decimal_places=2, max_digits=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userBid", null=True, blank=True)

    def __str__(self):
        return f"{self.bid }"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="currentbid", null=True, blank=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", null=True, blank=True)
    image = models.CharField(max_length=900)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", null=True, blank=True)
    watchlist = models.ManyToManyField(User, null=True, blank=True, related_name="watchlist")

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="author")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="comment")
    message = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"        