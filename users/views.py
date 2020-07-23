from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from users.models import Profile
import random
import json
import os.path


with open(os.path.dirname(__file__) + '/../parameters.json') as f:
    json = json.load(f)

words = json["keywords"]


def registerA(request):
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST['Username'],password=request.POST['Password'])
        user.save()
        keywords = str(random.sample(words, json["keywords_num"]))
        keywords = keywords.replace("'","").replace("]","").replace("[","")
        range_a, range_b = json['range']
        prices = random.choices(range(range_a,range_b), k=550)
        for i,val in enumerate(prices):
            if val>json["max"]:
                prices[i] = json["max"]
            elif val<json["min"]:
                prices[i]= json["min"]
        prices = str(prices).replace("]","").replace("[","")
        profile = Profile(user=user, group='A', keywords=keywords, prices=prices)
        profile.save()
        messages.success(request, f'Account created for {request.POST["Username"]}!')
        return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/registerA.html', {'form': form})


def registerB(request):
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST['Username'], password=request.POST['Password'])
        user.save()
        keywords = str(random.sample(words, json["keywords_num"])).replace("'", "").replace("]", "").replace("[", "")
        profile = Profile(user=user, group='B', keywords=keywords)
        profile.save()
        messages.success(request, f'Account created for {request.POST["Username"]}!')
        return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/registerB.html', {'form': form})