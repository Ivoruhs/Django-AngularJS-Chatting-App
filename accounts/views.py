import json
import urllib
from urllib import parse

from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls.base import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.models import UserInfo
from chatbox import settings
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View


class UserSignUp(View):
    form_class = UserForm
    template_name = 'signup.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        form = self.form_class(request.POST)
        imageFile = request.FILES.get('image', False)

        if form.is_valid():

            user = form.save(commit=False)
            username, email, password = form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password']
            user.set_password(password)
            user.save()

            if imageFile != False:
                userInfoObj = UserInfo()
                userInfoObj.userId = user
                userInfoObj.image = imageFile
                userInfoObj.save()

            return render(request, self.template_name, {'message': "Successfully registered!"})

        else:
            return render(request, self.template_name, {'message': "Form submission invalid!"})





class UserSignIn(View):
    form_class = UserForm
    template_name = 'signin.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('inbox')
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        username= request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password= password)

        if user is not None:
            login(request, user)
            return redirect('inbox')
        return render(request, self.template_name, {'message': "Username or password is not valid!"})





def UserSignOut(request):
    logout(request)
    return redirect('signin')


