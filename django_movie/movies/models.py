# Create your models here.
from django.db import models
from django.db.models.aggregates import Count
from datetime import date

from django.db.models.base import ModelState
class Category(models.Model):
    """Category"""
    name = models.CharField("Категория",max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Actor(models.Model):
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="actors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"

class Genre (models.Model):
    """Жанры"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

class Movie(models.Model):
    """Фильмы"""
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100,default='')
    description = models.TextField("описание")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    country = models.CharField("страна", max_length=50)
    directors = models.ManyToManyField(Actor,verbose_name="Режиссер", related_name="film_director")
    actors = models.ManyToManyField(Actor,verbose_name="Актеры", related_name="film_actor")
    genres = models.ManyToManyField(Genre,verbose_name="Жанры")
    world_premiere = models.DateField("Примьера в мире",default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="Указать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField("Сборы в США", default=0, help_text="Указать сумму в долларах")
    fees_in_world = models.PositiveIntegerField("Сборы в Мире", default=0, help_text="Указать сумму в долларах")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True) #On delete set null category
    url = models.SlugField(max_length=160,unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self) -> str:
        return super().__str__()

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(models.Model):
    """Кадры из фильма"""

    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("описание")
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie,verbose_name="Фильм",on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Кадры из фильма"
        verbose_name_plural = "Кадры из фильма"

class RatingStar(models.Model):
    """Звезды рейтинга"""
    value = models.PositiveSmallIntegerField("Value",default=0)

    def __str__(self) -> str:
        return self.value

    class Meta:
        verbose_name = "Звезды рейтинга"
        verbose_name_plural = "Звезды рейтинга"

class Rating(models.Model):
    """RAting"""
    ip = models.CharField("ИП Адрес",max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Звезда")
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,verbose_name="Фильм")

    def __str__(self) -> str:
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "рейтинг"
        verbose_name_plural = "рейтинги"

class Rewiews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL,blank=True,null=True) #self ссылается на запись в этой же таблице
    movie = models.ForeignKey(Movie,verbose_name="Фильм",on_delete=models.CASCADE) #отзывы удалятся вместе с фильмом

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"