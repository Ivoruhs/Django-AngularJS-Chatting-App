"""chatbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import accounts
from accounts import views
from django.conf.urls.static import static
from chatbox import settings

urlpatterns = [
    url(r'^signup/', accounts.views.UserSignUp.as_view(), name="signup"),
    url(r'^signout/', accounts.views.UserSignOut, name="signout"),
    url(r'^$', accounts.views.UserSignIn.as_view(), name="signin"),
    url(r'^chats/', include('chats.urls')),
    url(r'^admin/', admin.site.urls)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
