from django.shortcuts import render
import pickle
import essay
from .models import Post
from users.models import Profile
import json
import os.path


with open(os.path.dirname(__file__) + '/../parameters.json') as f:
    json = json.load(f)

with open("blog/essays.pickle", 'rb') as pickle_file:
    Essay_list = pickle.load(pickle_file)


def home(request):
    context = {'list': Essay_list}
    if request.method == 'POST' and '_Save' in request.POST:
        content = ''
        for i in range(len(Essay_list)):
            submitted = '0'
            if request.POST["decision {}".format(i)] == "yes":
                submitted = '2'
            elif request.POST["decision {}".format(i)] == "maybe":
                submitted = '1'
            content = content + submitted
        log = request.POST["log"]
        post = Post(id=str(request.user.id), content=str(content), log=log)
        post.save()
        profile = Profile(user=request.user, state=str(content), log=request.user.profile.log +"\n"+ log, keywords=request.user.profile.keywords,prices=request.user.profile.prices, group=request.user.profile.group)
        profile.save()
        print("success")
        if request.user.profile.group == 'A':
            return render(request, 'blog/home.html', context)
        elif request.user.profile.group == 'B':
            return render(request, 'blog/home2.html', context)
    elif request.method == 'POST' and '_sort-points' in request.POST:
        prices = request.user.profile.prices.split(",")
        prices = [int(i) for i in prices]
        zipped = list(zip(Essay_list, prices))
        zipped.sort(key=lambda x: x[1], reverse=True)
        res = list(zip(*zipped))
        context = {'list': res[0]}
        return render(request, 'blog/home.html', context)
    elif request.user.is_authenticated:
        if request.user.profile.group == 'A':
            return render(request, 'blog/home.html', context)
        elif request.user.profile.group == 'B':
            return render(request, 'blog/home2.html', context)
        else:
            return render(request, 'blog/blank.html', context)
    else:
        return render(request, 'blog/blank.html', context)


def instructions(request):
    context = {'papers_get': json["papers_get"],'money': json["money"],'extra_money_per_word_1': json["extra_money_per_word_1"],'budget': json["budget"],
               'paper_num_to_choose': json["paper_num_to_choose"],'extra_money_per_word_2': json["extra_money_per_word_2"],'deduct_money': json["deduct_money"]}
    if request.user.is_authenticated:
        if request.user.profile.group == 'A':
            return render(request, 'blog/Ainstructions.html', context)
        elif request.user.profile.group == 'B':
            return render(request, 'blog/Binstructions.html', context)
    else:
        return render(request, 'blog/blank.html', context)



def Binstructions(request):
    context = {'papers_get': json["papers_get"],'money': json["money"],'extra_money_per_word_1': json["extra_money_per_word_1"],'paper_num_to_choose': json["paper_num_to_choose"]
               ,'extra_money_per_word_2': json["extra_money_per_word_2"],'deduct_money': json["deduct_money"]}
    return render(request, 'blog/Binstructions.html')


def blank(request):
    return render(request, 'blog/blank.html')