from django.contrib import admin

from watchlist_app.models import WatchList, StreamPlatForm
# Register your models here.
admin.site.register(WatchList)
admin.site.register(StreamPlatForm)