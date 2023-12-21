from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("categories", views.categories, name="categories"),
    path("filter/<int:category_id>/", views.filter, name="filter"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("remove/<int:id>", views.remove, name="remove"),
    path("add/<int:id>", views.add, name="add"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("close/<int:id>", views.close, name="close")        
] 