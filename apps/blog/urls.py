from django.conf.urls import url
from apps.blog import views

app_name = 'blog'
urlpatterns = [
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^logout/', views.LogOutView.as_view(), name='logout'),
    url(r'^register/', views.RegisterView.as_view(), name='register'),

    url(r'^index/', views.IndexCenterView.as_view(), name='indexcenter'),
    url(r'^indexclassify/(?P<classify>[0-9]+)/?$',
        views.IndexClassify.as_view(), name='indexclassify'),
    url(r'^timeline/', views.TimeLineView.as_view(), name='timeline'),
    url(r'^article/(?P<art_date>[0-9]{8})/(?P<pinyin_title>.+)/?$',
        views.ArticleView.as_view(), name='article'),

    url(r'^test/', views.testview, name='testview'),
]
