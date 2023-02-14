from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("time/<uuid:uuid>", views.abstinence_time, name="abstinence_time"),
    path("stop/<uuid:uuid>", views.stop, name="stop"),
    path("reset/<uuid:uuid>", views.reset, name="reset"),

    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("history/", views.history, name="history"),
    path("start-new/", views.new, name="start-new"),
    path("trophies/", views.trophies, name="trophies"),
    path("check-trophies/", views.check_trophies, name="check-trophies"),
    path("overview/", views.abstincence_overview, name="overview"),

    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("resources/", views.resources, name="resources"),
]
