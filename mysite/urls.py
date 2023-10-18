from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('utils/', include("utils.urls")),
    # path('admin/', admin.site.urls),
]
