from django.urls import path

from . import views

app_name = "utils"
urlpatterns = [
    path("", views.index, name="index"),
    path("returnMetadata/", views.returnMetadata, name="returnMetadata"),
    path("returnContent/", views.returnContent, name="returnContent"),
    path("returnTransformation/", views.returnTransformation, name="returnTransformation"),
    path("returnSecurity/", views.returnSecurity, name="returnSecurity")
]
