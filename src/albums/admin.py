from django.contrib import admin
from . models import Singer, Song, SongNumber, Album


@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    fields = ['name']
    list_filter = ('name',)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    fields = ['name']
    list_filter = ('name',)


@admin.register(SongNumber)
class SongNumberAdmin(admin.ModelAdmin):
    list_display = ('id', 'album', 'song', 'number_song',)
    fields = ['album', 'song', 'number_song']
    list_filter = ('album', 'song',)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'singer',)
    fields = ['name', 'year', 'singer']
    list_filter = ('year', 'singer')
