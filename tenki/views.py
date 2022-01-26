from django.shortcuts import render
from django.views import View

from .models import Weather
from .forms import YearMonthForm

from django.core.paginator import Paginator 
from django.db.models.functions import TruncMonth
from django.db.models import Avg



class IndexView(View):

    def get(self, request, *args, **kwargs):

        context = {}

        #ページ上部に最新の天気を数件表示させる
        #context["weather"]  = Weather.objects.order_by("-dt").first()
        context["weathers"] = Weather.objects.order_by("-dt")[:3]

        weathers = Weather.objects.filter(dt__year="2022",dt__month="13").order_by("-dt")
        print(weathers)

        if "year" in request.GET:
            print(type(request.GET["year"]))
            print(request.GET["year"])

        #ここで年月検索を行う。パラメーターの値をバリデーション、未指定もしくは間違った値が指定されている場合、全て表示させる。
        form    = YearMonthForm(request.GET)
        if form.is_valid():
            cleaned         = form.clean()
            all_weathers    = Weather.objects.filter(dt__year=cleaned["year"],dt__month=cleaned["month"]).order_by("-dt")
        else:
            all_weathers    = Weather.objects.order_by("-dt")


        #1ページ表示させるページ数を指定
        paginator   = Paginator(all_weathers,3)

        #何ページ目を表示させるかの指定
        if "page" in request.GET:
            all_weathers    = paginator.get_page(request.GET["page"])
        else:
            all_weathers    = paginator.get_page(1)
        
        #TODO:ここでページネーションを実装する。ただし、検索機能とページ移動を両立させなければならない。
        #https://noauto-nolife.com/post/django-paginator/
        context["all_weathers"] = all_weathers


        #年月入力のための最古と最新データを抜き取り、年月のリストを作る。
        oldest_dt   = Weather.objects.order_by("dt").first().dt
        newest_dt   = Weather.objects.order_by("-dt").first().dt

        oldest_year = oldest_dt.year
        newest_year = newest_dt.year
        print(oldest_year)
        print(newest_year)
        
        """
        years   = []
        for i in range(newest_year,oldest_year-1,-1):
            years.append(i)

        context["years"]    = years
        """

        #リストの内包表記
        #https://note.nkmk.me/python-list-comprehension/
        context["months"]   = [ i for i in range(1,13) ]
        context["years"]    = [ i for i in range(newest_year,oldest_year-1,-1) ]


        #月ごとの平均気温の出力(TruncMonthで月ごとに集計し、最高気温と最低気温の平均を生成、最後に月でソーティングする。)
        #https://noauto-nolife.com/post/django-models-trunc/
        monthly_temp  = Weather.objects.annotate(monthly=TruncMonth("dt")).values("monthly").annotate(
                    today_high_temp_avg = Avg("today_high_temp"),today_low_temp_avg = Avg("today_low_temp")
                    ).values("monthly","today_high_temp_avg","today_low_temp_avg").order_by("-monthly")

        print(monthly_temp)

        return render(request,"tenki/index.html",context)

index   = IndexView.as_view()
