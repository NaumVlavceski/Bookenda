"""
URL configuration for EventsReservation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("django.contrib.auth.urls")),
    path("register/",views.register,name="register"),
    path("events/",views.events,name="events"),
    path("event_detail/<id>",views.event_detail,name="event_detail"),
    path("delete_event/<id>",views.delete_event,name="delete_event"),
    path("add_event/",views.add_event,name="add_event"),
    path("edit_event/<id>",views.edit_event,name="edit_event"),
    path("",views.index,name="index"),
    path("profile/",views.profile, name="profile"),
    path("remove_reservation/<id>",views.remove_reservation, name="remove_reservation"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
