from django.contrib import admin

from .models import Weather

class WeatherAdmin(admin.ModelAdmin):

    list_display = ["place","dt","today","today_high_temp","today_low_temp","tomorrow","tomorrow_high_temp","tomorrow_low_temp"]

    search_fields = [ "place" ]
    list_filter   = [ "today","tomorrow" ]

    list_per_page       = 10
    list_max_show_all   = 20000

admin.site.register(Weather,WeatherAdmin)
