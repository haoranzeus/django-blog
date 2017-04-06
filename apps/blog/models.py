import markdown
import pinyin
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ArticleModel(models.Model):
    title = models.CharField('title', max_length=50)
    head_img = models.CharField('hand image', max_length=150)
    quote_title = models.CharField(
            'quote title', max_length=100, null=True, blank=True)
    quote = models.TextField('quote')
    quote_cite = models.CharField(
            'quote_cite', max_length=40, null=True, blank=True)
    quote_footer = models.CharField(
            'quote_footer', max_length=100, null=True, blank=True)
    article_md = models.TextField('markdown article text')
    article_html = models.TextField('html article text', default='')
    is_valid = models.BooleanField('if is valid', default=True)
    create_time = models.DateTimeField('create time')
    modify_time = models.DateTimeField('modify time', auto_now=True)
    tag = models.ManyToManyField('TagModel', related_name='article')
    pinyin_title = models.CharField('initial pinyin title', max_length=100,
                                    default='')
    classify = models.ForeignKey(
            'Classify', on_delete=models.CASCADE, related_name='article')

    def save(self, *args, **kwargs):
        if not self.id:
            self.create_time = timezone.now()
        self.article_html = markdown.markdown(self.article_md)
        self.pinyin_title = ''
        for i in filter(
                str.isalnum, pinyin.get_initial(self.title, delimiter='')):
            self.pinyin_title += i
        super(ArticleModel, self).save(args, kwargs)

    @property
    def create_data(self):
        return self.create_time.strftime('%Y%m%d')

    # @property
    # def pinyin_title(self):
    #     return pinyin.get_initial(self.title, delimiter='')

    class Meta:
        db_table = 'article'


class Classify(models.Model):
    name = models.CharField('classification name', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'classify'


class TagModel(models.Model):
    tag = models.CharField('article tag', max_length=20)

    def __str__(self):
        return self.tag

    class Meta:
        db_table = 'tag'


class Comment(models.Model):
    comment = models.CharField('comment content', max_length=190)
    article = models.ForeignKey(
            'ArticleModel',  on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(
            User, on_delete=models.CASCADE, related_name='comment')
    create_time = models.DateTimeField('create time', auto_now_add=True)
