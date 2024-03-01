from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Comment, Watch


def index(request):
    auctions = Auction.objects.all()
    return render(request, "auctions/index.html", {
        "activeAuctions": auctions
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def auction(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    watchers = auction.watchers.all()
    comments = auction.comments.all()
    watching = False
    if watchers and request.user.is_authenticated:
        for watcher in watchers:
            if request.user.pk == watcher.user.pk:
                watching = True
    return render(request, "auctions/listing.html", {
        "auction": auction,
        "watchers": watchers,
        "watching": watching,
        "comments": comments
    })

def createListing(request):
    if request.method == "POST":
        name = request.POST["auctionName"]
        price = request.POST["startingPrice"]
        user = User.objects.get(username=request.POST["username"])
        auction = Auction(auctionName=name, startingPrice=price, creator=user)
        auction.save()
        # auction_ID = Auction.objects.get()
        return HttpResponseRedirect(reverse("auction", args=(auction.pk,)))
    return render(request, "auctions/createListing.html")

def addComment(request, auction_id):
    if request.method == "POST":
        user = User.objects.get(username=request.POST["username"])
        commentText = request.POST["commentText"]
        auction = Auction.objects.get(pk=auction_id)
        newComment = Comment(text=commentText, auction=auction, user=user)
        newComment.save()
        return HttpResponseRedirect(reverse("auction", args=(auction_id,)))
    
def watch(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(pk=auction_id)
        user = User.objects.get(username=request.POST["username"])
        if auction.watchers:
            watchers = auction.watchers.all()
            found = False
            for watcher in watchers:
                if user.pk == watcher.user.pk:
                    found = True
            if found == False:  
                watch = Watch(auction=auction, user=user)
                watch.save()
        else:
            watch = Watch(auction=auction, user=user)
            watch.save()
        return HttpResponseRedirect(reverse("auction", args=(auction_id,)))
    
def unwatch(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(pk=auction_id)
        user = User.objects.get(username=request.POST["username"])
        if auction.watchers:
            watchers = auction.watchers.all()
            for watcher in watchers:
                if user.pk == watcher.user.pk:
                    watcher.delete()
        return HttpResponseRedirect(reverse("auction", args=(auction_id,)))