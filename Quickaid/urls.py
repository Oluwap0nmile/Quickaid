"""
URL configuration for Quickaid project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from users.views import emergency_contact_view
from django.urls import path,include
from pages.views import (
    index,
    contact,
    department,
    about,
    services,
    logout_view
  


)
from users.views import (
    register,
    login_view,
    emergency_contact_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name= 'home'),
    path('about/', about, name= 'about'),
    path('contact/', contact, name= 'contact'),
    path('department/',department ,name='department'),
    path('services/',services , name='services'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/', include('users.urls')),
    path('emergency_contact/', emergency_contact_view, name='emergency_contact'),
    
    
    
    
]
