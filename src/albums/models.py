from datetime import datetime as dt
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


def year_validator(year: int) -> int:
    '''Проверка того, что указанный год не превышает текущий.'''
    if year > dt.now().year:
        raise ValidationError(
            'Год выхода альбома не может превышать текущий.'
        )
    return year


class Singer(models.Model):
    '''Модель исполнителя.'''
    name = models.CharField(
        max_length=48,
        verbose_name='Название исполнителя',
        unique=True,
    )

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'

    def __str__(self) -> str:
        return self.name


class Song(models.Model):
    """Модель песни."""
    name = models.CharField(
        max_length=48,
        verbose_name='Название песни'
    )

    class Meta:
        verbose_name = 'Песня'
        verbose_name_plural = 'Песни'

    def __str__(self) -> str:
        return self.name


class SongNumber(models.Model):
    '''Модель для связи песни и её номера в альбоме.'''
    album = models.ForeignKey(
        'Album',
        on_delete=models.CASCADE,
        verbose_name='Альбом'
    )
    song = models.ForeignKey(
        'Song',
        on_delete=models.CASCADE,
        verbose_name='Песня'
    )
    number_song = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1)
        ],
        verbose_name='Порядковый номер песни в альбоме',
    )

    class Meta:
        ordering = ('album',)
        verbose_name = 'Связь альбома и песни'
        verbose_name_plural = 'Связи альбомов и песен'
        constraints = [
            models.UniqueConstraint(fields=['album', 'song'],
                                    name=('unique song in album')),
            models.UniqueConstraint(fields=['album', 'number_song'],
                                    name=('unique number_song in album')),
        ]

    def __str__(self) -> str:
        return f'{self.song} относится к альбому {self.album}'


class Album(models.Model):
    '''Модель альбома.'''
    name = models.CharField(
        max_length=48,
        verbose_name='Название альбома'
    )
    year = models.PositiveIntegerField(
        validators=[year_validator],
        verbose_name='Год выхода')
    singer = models.ForeignKey(
        Singer,
        on_delete=models.CASCADE,
        verbose_name='Исполнитель альбома',
        related_name='albums'
    )
    songs = models.ManyToManyField(
        Song,
        through=SongNumber,
        related_name='albums'
    )

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'
        constraints = [
            models.UniqueConstraint(fields=['name', 'year', 'singer'],
                                    name=('unique name year singer in album')),
        ]

    def __str__(self) -> str:
        return self.name
