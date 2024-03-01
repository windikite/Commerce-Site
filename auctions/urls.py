from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:auction_id>", views.auction, name="auction"),
    path("createListing", views.createListing, name="createListing"),
    path("addComment/<int:auction_id>", views.addComment, name="addComment"),
    path("watch/<int:auction_id>", views.watch, name="watch"),
    path("unwatch/<int:auction_id>", views.unwatch, name="unwatch"),
]
