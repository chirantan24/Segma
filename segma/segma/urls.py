"""segma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from segmapp import views
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('login/',auth_view.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_view.LogoutView.as_view(),name='logout'),
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('app/',include('segmapp.urls')),
    path('bio/',views.make_bio.as_view(),name='bio'),
    path('biodetail/<pk>',views.BioDetail.as_view(),name='biodetail'),
    path('requests/',views.RequestList.as_view(),name='requests'),
    path('followers/',views.Followerlist.as_view(),name='followers'),
    path('profile/<pk>',views.UserDetail.as_view(),name='profile'),
    path('search/',views.SearchResults.as_view(),name='search')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
