import os
import datetime
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import LoginForm, RegisterForm
from .models import ArticleModel, Classify

# Create your views here.


def testview(request):
    if request.method == 'POST':
        print(request.POST)
        # username = request.POST['username']
        # password = request.POST['password']
        # user = authenticate(username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     render('redirect html')
        # else:
        #     render('return login error message')
    elif request.method == 'GET':
        return render(request, 'login.html')


class LoginView(View):
    template_name = 'auth/login.html'

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username, password)
        return render(request, self.template_name, self.kwargs)

    def get(self, request):
        kwargs = {
            'blog_name': os.environ.get('BLOG_NAME', 'AmazeUI')
        }
        return render(request, self.template_name, kwargs)


class RegisterView(View):
    template_name = 'auth/register.html'

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 != password2:
                print('password mismatch')
            else:
                try:
                    user = User.objects.create_user(username, '', password1)
                except IntegrityError:
                    kwargs = {
                        'blog_name': os.environ.get('BLOG_NAME', 'AmazeUI'),
                        'username_unusable': True,
                    }
                    return render(request, self.template_name, kwargs)
                user.save()
                login(request, user)
        else:
            print('form errror')
            kwargs = {
                'blog_name': os.environ.get('BLOG_NAME', 'AmazeUI')
            }
            return render(request, self.template_name, kwargs)
        return HttpResponseRedirect(reverse('testview'))

    def get(self, request):
        kwargs = {
            'blog_name': os.environ.get('BLOG_NAME', 'AmazeUI')
        }
        return render(request, self.template_name, kwargs)


class IndexCenterView(View):
    template_name = 'blog/index.html'

    def get(self, request):
        articles = ArticleModel.objects.all()
        paginator = Paginator(articles, 5)
        page = request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        classifications = Classify.objects.all()
        kwargs = {
            'page_obj': page_obj,
            'classifications': classifications,
        }
        return render(request, self.template_name, kwargs)


class IndexClassify(View):
    template_name = 'blog/index.html'

    def get(self, request, classify):
        articles = ArticleModel.objects.filter(classify=classify)
        paginator = Paginator(articles, 5)
        page = request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        classifications = Classify.objects.all()
        kwargs = {
            'page_obj': page_obj,
            'classifications': classifications,
        }
        return render(request, self.template_name, kwargs)


class TimeLineView(View):
    template_name = 'blog/timeline.html'

    def get(self, request):
        articles = ArticleModel.objects.all().order_by('-create_time')
        classifications = Classify.objects.all()
        kwargs = {
            'articles': articles,
            'classifications': classifications,
        }
        return render(request, self.template_name, kwargs)


class ArticleView(View):
    template_name = 'blog/article.html'

    def get(self, request, art_date, pinyin_title):
        year = int(art_date[:4])
        month = int(art_date[4:6])
        day = int(art_date[6:])
        article = get_object_or_404(
                ArticleModel,
                create_time__date=datetime.date(year, month, day),
                pinyin_title=pinyin_title)
        tags = article.tag.all()
        article_prev = ArticleModel.objects.filter(id__lt=article.id).last()
        article_next = ArticleModel.objects.filter(id__gt=article.id).first()
        classifications = Classify.objects.all()
        kwargs = {
            'article': article,
            'tags': tags,
            'article_prev': article_prev,
            'article_next': article_next,
            'classifications': classifications,
        }
        return render(request, self.template_name, kwargs)
