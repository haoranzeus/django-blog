import os
import datetime
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import LoginForm, RegisterForm, CommentForm
from .models import ArticleModel, Classify, Comment, TagModel

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


class HomeView(View):
    def get(self, request):
        return HttpResponseRedirect(reverse('blog:indexcenter'))


class LoginView(View):
    template_name = 'auth/login.html'

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # user = get_object_or_404(User, email=email)
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    next = request.GET.get('next')
                    return redirect(next)
                except:
                    return HttpResponseRedirect(reverse('blog:indexcenter'))
            else:
                return render(request, self.template_name, self.kwargs)
                

    def get(self, request):
        kwargs = {
            'blog_name': os.environ.get('BLOG_NAME', 'AmazeUI')
        }
        return render(request, self.template_name, kwargs)


class LogOutView(View):
    def get(self, request):
        logout(request)
        try:
            next = request.GET.get('next')
            return redirect(next)
        except:
            return HttpResponseRedirect(reverse('blog:indexcenter'))


class RegisterView(View):
    template_name = 'auth/register.html'

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email_user = User.objects.filter(email=email)
            if email_user != []:
                kwargs = {
                    'blog_name': os.environ.get('BLOG_NAME', 'AmazeUI'),
                    'email_unusable': True,
                }
                return render(request, self.template_name, kwargs)
            if password1 != password2:
                print('password mismatch')
            else:
                try:
                    user = User.objects.create_user(username, email, password1)
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
        return HttpResponseRedirect(reverse('blog:indexcenter'))

    def get(self, request):
        kwargs = {
            'blog_name': os.environ.get('BLOG_NAME', 'AmazeUI')
        }
        return render(request, self.template_name, kwargs)


class IndexCenterView(View):
    template_name = 'blog/index.html'

    def get(self, request):
        articles = ArticleModel.objects.order_by('-create_time')
        paginator = Paginator(articles, 10)
        page = request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        classifications = Classify.objects.all()
        tags = TagModel.objects.all()
        kwargs = {
            'page_obj': page_obj,
            'classifications': classifications,
            'current_path': request.path,
            'tags': tags,
        }
        if request.user.is_authenticated:
            kwargs['logged'] = True
        else:
            kwargs['logged'] = False
        return render(request, self.template_name, kwargs)


class IndexClassify(View):
    template_name = 'blog/index.html'

    def get(self, request, classify):
        articles = ArticleModel.objects.filter(classify=classify).order_by(
                '-create_time')
        paginator = Paginator(articles, 10)
        page = request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        classifications = Classify.objects.all()
        tags = TagModel.objects.all()
        kwargs = {
            'page_obj': page_obj,
            'classifications': classifications,
            'current_path': request.path,
            'tags': tags,
        }
        if request.user.is_authenticated:
            kwargs['logged'] = True
        else:
            kwargs['logged'] = False
        return render(request, self.template_name, kwargs)


class IndexTag(View):
    """
    index page when click a tag
    """
    template_name = 'blog/index.html'

    def get(self, request, tag):
        articles = ArticleModel.objects.filter(tag=tag).order_by('-create_time')
        paginator = Paginator(articles, 10)
        page = request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        classifications = Classify.objects.all()
        tags = TagModel.objects.all()
        kwargs = {
            'page_obj': page_obj,
            'classifications': classifications,
            'current_path': request.path,
            'tags': tags,
        }
        if request.user.is_authenticated:
            kwargs['logged'] = True
        else:
            kwargs['logged'] = False
        return render(request, self.template_name, kwargs)


class TimeLineView(View):
    template_name = 'blog/timeline.html'

    def get(self, request):
        articles = ArticleModel.objects.all().order_by('-create_time')
        classifications = Classify.objects.all()
        kwargs = {
            'articles': articles,
            'classifications': classifications,
            'current_path': request.path,
        }
        if request.user.is_authenticated:
            kwargs['logged'] = True
        else:
            kwargs['logged'] = False
        return render(request, self.template_name, kwargs)


class ArticleView(View):
    template_name = 'blog/article.html'

    def render_kwargs(self, request, art_date, pinyin_title):
        year = int(art_date[:4])
        month = int(art_date[4:6])
        day = int(art_date[6:])
        article = get_object_or_404(
                ArticleModel,
                # create_time__date=datetime.date(year, month, day),
                create_time__year=year,
                pinyin_title=pinyin_title)
        tags = article.tag.all()
        article_prev = ArticleModel.objects.filter(id__lt=article.id).last()
        article_next = ArticleModel.objects.filter(id__gt=article.id).first()
        classifications = Classify.objects.all()
        comments = Comment.objects.filter(article=article)
        kwargs = {
            'article': article,
            'tags': tags,
            'article_prev': article_prev,
            'article_next': article_next,
            'classifications': classifications,
            'comments': comments,
            'current_path': request.path,
        }
        if request.user.is_authenticated:
            kwargs['logged'] = True
        else:
            kwargs['logged'] = False
        return kwargs

    def get(self, request, art_date, pinyin_title):
        kwargs = self.render_kwargs(request, art_date, pinyin_title)
        return render(request, self.template_name, kwargs)

    def post(self, request, art_date, pinyin_title):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            user = request.user
            kwargs = self.render_kwargs(request, art_date, pinyin_title)
            Comment.objects.create(
                    comment=comment, article=kwargs['article'], user=user)
            return redirect(request.path)
