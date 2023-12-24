from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Listing, Category, Comment, Bid


def index(request):
    active = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": active
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

@login_required
def create(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        image  = request.POST["image"]
        price = request.POST["price"]
        category = request.POST["category"]
        categories = Category.objects.get(categoryType=category)
        sessionUser = request.user

        bid = Bid(bid=float(price), user=sessionUser)
        bid.save()

        listing = Listing(
            title=title,
            description=description,
            image=image,
            price=bid,
            category=categories,
            owner=sessionUser 
        )
        listing.save()
        return HttpResponseRedirect(reverse(index))

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def listing(request, id):
    viewListing = Listing.objects.get(pk=id)
    checkWatchlist = request.user in viewListing.watchlist.all()
    viewComments = Comment.objects.filter(listing=viewListing)
    checkSeller = request.user.username == viewListing.owner.username
    return render(request, "auctions/listing.html", {
        "listing": viewListing,
        "checkWatchlist": checkWatchlist,        
        "viewComments": viewComments,
        "checkSeller": checkSeller
    })

def filter(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    viewFilter = Listing.objects.filter(active=True, category=category)
    categories = Category.objects.all()
    return render(request, "auctions/filter.html", {
        "listings": viewFilter,
        "categories": categories,
        "category": category
})

@login_required
def watchlist(request):
    sessionUser = request.user
    listings = sessionUser.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required
def add(request, id):
    viewListing = Listing.objects.get(pk=id)
    sessionUser = request.user
    viewListing.watchlist.add(sessionUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))
    

@login_required
def remove(request, id):
    viewListing = Listing.objects.get(pk=id)
    sessionUser = request.user
    viewListing.watchlist.remove(sessionUser)
    return HttpResponseRedirect(reverse(listing, args=(id, )))

@login_required
def comment(request, id):
    sessionUser = request.user
    viewListing = Listing.objects.get(pk=id)
    message = request.POST['newComment']
    
    newComment = Comment(
        author=sessionUser,
        listing=viewListing, 
        message=message
    )
    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))

@login_required
def bid(request, id):
    userBid = request.POST['newBid']
    viewListing = Listing.objects.get(pk=id)
    checkWatchlist = request.user in viewListing.watchlist.all()
    viewComments = Comment.objects.filter(listing=viewListing)
    checkSeller = request.user.username == viewListing.owner.username
    if int(userBid) > viewListing.price.bid:
        sessionUser = request.user
        viewListing.watchlist.add(sessionUser)
        update = Bid(user=request.user, bid=userBid)
        update.save()
        viewListing.price = update
        viewListing.save()        
        return render(request, "auctions/listing.html", {
            "listing": viewListing,
            "message": "Your bid was accepted",
            "update": True,
            "checkWatchlist": checkWatchlist,        
            "viewComments": viewComments,
            "checkSeller": checkSeller
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": viewListing,
            "message": "Bid must be higher than the current bid amount. Your bid attempt was unsuccessful",
            "update": False,
            "checkWatacahlislt": checkWatchlist,        
            "viewComments": viewComments,
            "checkSeller": checkSeller
        })
    
def close(request, id):
    viewListing = Listing.objects.get(pk=id)
    viewListing.active = False
    viewListing.save()
    checkWatchlist = request.user in viewListing.watchlist.all()
    viewComments = Comment.objects.filter(listing=viewListing)
    checkSeller = request.user.username == viewListing.owner.username
    return render(request, "auctions/listing.html", {
        "listing": viewListing,
        "checkWatchlist": checkWatchlist,        
        "viewComments": viewComments,
        "checkSeller": checkSeller,
        "update": True,
    })