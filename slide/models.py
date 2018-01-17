from django.db import models


class Slide(models.Model):
    alias = models.CharField(max_length=200, unique=True, verbose_name="访问的url")
    title = models.CharField(max_length=200, verbose_name="标题")
    hide = models.BooleanField(default=True, verbose_name="是否隐藏")
    style = models.TextField(blank=True, verbose_name="补充样式，css")
    config = models.CharField(max_length=200, blank=True, verbose_name="配置")
    content = models.TextField(verbose_name="正文", help_text="必须为Markdown格式，参考:https://remarkjs.com/")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = verbose_name = 'slide'
