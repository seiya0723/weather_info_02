from django.db import models
from django.utils import timezone


class Weather(models.Model):

    place = models.CharField(verbose_name="場所",max_length=20)
    dt    = models.DateTimeField(verbose_name="投稿日",default=timezone.now)
    today = models.CharField(verbose_name="今日の天気",max_length=150)
    tomorrow = models.CharField(verbose_name="明日の天気",max_length=150)

    today_high_temp = models.IntegerField(verbose_name="今日の最高気温(℃)")
    today_low_temp = models.IntegerField(verbose_name="今日の最低気温(℃)")
    tomorrow_high_temp = models.IntegerField(verbose_name="明日の最高気温(℃)")
    tomorrow_low_temp = models.IntegerField(verbose_name="明日の最低気温(℃)")

    """
    def __str__(self):
        return self.place
    """
