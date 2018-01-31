from django.shortcuts import render,redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.views.generic import *
from .models import *
import logging
from django.core.urlresolvers import reverse_lazy,reverse
from django.views import generic
from pusher import Pusher
import json


class UserRegisterView(View):
    form_class = UserForm
    template_name = 'home/registration.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, { 'form' : form })

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            user.set_password(password)
            user.save()

            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home:feed', user.pk)

        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    template_name = 'home/login.html'
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form= self.form_class(request.POST)
        logger = logging.getLogger(__name__)

        logger.error("hiiiiiiiiiiiiii")
        username = request.POST['username']
        password = request.POST['password']
        logger.error(username)
        logger.error(password)
        user = authenticate(username=username, password=password)
        logger.error(user)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home:feed', user.pk)


        return render(request, self.template_name, {'form': form})

    def get_absolute_url(self):
        return reverse('home:login')


class PostView(CreateView):
   form_class = PostForm
   template_name = 'home/feedModel_form.html'


   def get(self, request, *args, **kwargs):
       form=self.form_class(None)
       return render(request, self.template_name, {'form':form })

   def post(self, request, *args, **kwargs):
       logger = logging.getLogger(__name__)
       form = self.form_class(request.POST, request.FILES)

       if form.is_valid():
           user=request.user
           self.object=form.save(commit=False)
           self.object.user=user
           self.object.save()
           logger.error("voilaaaaaaaaaaaaaaaa!")
           return redirect('home:feed', user_id=user.id)


       return render(request, self.template_name, {'form':form })


def feedview(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'home/feed.html', {'user': user})


def followUser(request, user_id):
    user = User.objects.get(pk=user_id)
    logger = logging.getLogger(__name__)
    a = ExtraInfoUser.objects.filter(following=user, follows=request.user)
    logger.error(a)
    logger.error(next)
    for obj in a:
        if obj.follows==request.user:
            obj.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        logger.error("bvbvbvb")
        a=ExtraInfoUser(following=user)
        a.save()
        request.user.follows.add(a)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def likeview(request, feedmodel_id):
    feedmodel = FeedModel.objects.get(pk=feedmodel_id)
    a = Likes.objects.filter(user=request.user, feedmodel=feedmodel)
    for obj in a:
        feedmodel.like= feedmodel.like-1
        feedmodel.save()
        a.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    a=Likes(user=request.user, feedmodel=feedmodel)
    a.save()
    feedmodel.like= feedmodel.like+1
    feedmodel.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AccountView(generic.DetailView):
    model = User
    template_name = 'home/account.html'