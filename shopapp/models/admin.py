from django.contrib import admin
from .models import Books

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'stock')
    search_fields = ('title', 'author__name')
    prepopulated_fields = {'slug': ('title',)}
