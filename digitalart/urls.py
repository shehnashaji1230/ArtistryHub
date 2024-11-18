"""
URL configuration for digitalart project.

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
from gallery import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpView.as_view(),name='signup'),
    path('signin/',views.SignInView.as_view(),name='login'),
    path('artist/dashboard/',views.ArtistDashboardView.as_view(),name='artist-dashboard'),
    path('customer/dashboard/',views.CustomerDashboardView.as_view(),name='customer-dashboard'),
    path('logout/',views.SignOutView.as_view(),name='logout'),
    path('profile/change',views.ProfileEditView.as_view(),name='profile-edit'),
    path('myprofile/',views.MyProfileView.as_view(),name='profile-view'),
    path('category/add/',views.CategoryView.as_view(),name='category-create'),
    path('artworks/add/',views.ArtWorkCreateView.as_view(),name='artwork-create'),
    path('myartworks/all/',views.MyArtWorkListView.as_view(),name='artwork-list'),
    path('artwork/<int:pk>/change/',views.ArtWorkUpdateView.as_view(),name='artwork-update'),
    path('artwork/<int:pk>/remove/',views.MyArtWorkDeleteView.as_view(),name='artwork-delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
