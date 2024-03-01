from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Auction(models.Model):
    auctionName = models.CharField(max_length=64)
    startingPrice = models.IntegerField()
    creator = models.ForeignKey(
        User,
        blank=True,
        on_delete=models.CASCADE,
        related_name="auctions")

    def __str__(self):
        return f"{self.auctionName}"
    
    
class Watch(models.Model):
    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name="watchers")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="watchlist"
    )
    
    def __str__(self):
        return f"{self.user} is watching {self.auction}"

class Bid(models.Model):
    amount = models.IntegerField()
    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name="bids")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bids"
    )
    
    def __str__(self):
        return f"A bid for {self.amount} on {self.auction} by {self.user}"
    
class Comment(models.Model):
    text = models.CharField(max_length=200)
    auction = models.ForeignKey(
        Auction, 
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    def __str__(self):
        return f"{self.user}: {self.text}"