from django.contrib import admin
from friends.models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass
