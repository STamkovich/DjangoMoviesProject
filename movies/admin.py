from django.contrib import admin
from django.utils.safestring import mark_safe

from django import forms
from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    """Отзывы на странице фильма"""
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


class MoviShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ["get_image"]

    def get_image(self, odj):
        return mark_safe(f'<img src={odj.image.url} width="200" height="120"')

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category",)
    search_fields = ("title", "category__name")
    inlines = [MoviShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    form = MovieAdminForm
    # fields = (("actors", "directors", "genres"),)
    fieldsets = (
        (None, {
            "fields": [("title", "tagline")]
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )
    readonly_fields = ["get_image"]

    def get_image(self, odj):
        return mark_safe(f'<img src={odj.poster.url} width="100" height="200"')

    get_image.short_description = "Постер"


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("movie", "ip", "star")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актёры"""
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, odj):
        return mark_safe(f'<img src={odj.image.url} width="200" height="120"')

    get_image.short_description = "Изображение"


@admin.register(RatingStar)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "value")


@admin.register(MovieShots)
class MovieShots(admin.ModelAdmin):
    list_display = ("title", "description", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, odj):
        return mark_safe(f'<img src={odj.image.url} width="200" height="120"')

    get_image.short_description = "Изображение"


admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
