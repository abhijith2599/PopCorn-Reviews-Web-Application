"""
URL configuration for Movie_Review project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from Movie_App.views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('PopCornReview/home/',Home_view.as_view(),name='home'),
    
    path('PopCornReview/signup/',UserRegistration_view.as_view(),name='signup'),
    path('PopCornReview/login/',Login_view.as_view(),name='login'),
    path('PopCornReview/logout/',Logout_view.as_view(),name='logout'),

    path('PopCornReview/userpage/',Userpage_view.as_view(),name='userpage'),
    path('PopCornReview/add_review/<int:pk>',AddReview_view.as_view(),name='add_review'),
    # path('PopCornReview/update_review/<int:pk>',UpdateReview_view.as_view(),name='update_review'),
    path('PopCornReview/delete_review/<int:pk>',DeleteReview_view.as_view(),name='delete')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# This allows Django to serve media files (like uploaded images) only during development.

# In production, you need to use a real web server like NGINX or AWS S3 to serve media files.