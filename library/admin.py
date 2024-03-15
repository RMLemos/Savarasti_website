from django.contrib import admin
from library.models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'country', 'bio',
    list_display_links = 'name',
    search_fields = 'name', 'country',
    list_per_page = 10
    ordering = 'name',
    readonly_fields = (
        'created_at', 'updated_at',
    )

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'publisher', 'nr_pages', 'isbn', 'synopsis',
    list_display_links = 'title',
    search_fields = 'title', 'isbn',
    list_per_page = 10
    ordering = 'title',
    readonly_fields = (
        'created_at', 'updated_at',
    )
    autocomplete_fields = 'author',
