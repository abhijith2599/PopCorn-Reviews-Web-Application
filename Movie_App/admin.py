from django.contrib import admin

from .models import Movies,Review

class MovieAdmin(admin.ModelAdmin):
    list_display=('M_name','M_lang','Director','Released_date','Genre')
    search_fields = ('M_name', 'Genre', 'Director')


class ReviewAdmin(admin.ModelAdmin):
    list_display=('user_id', 'movie_id','comments', 'rating', 'created_date')

admin.site.register(Movies,MovieAdmin)
admin.site.register(Review,ReviewAdmin)

# Register your models here.

# Registers the Movies model in Django Admin.

# Customizes the admin panel:

# list_display = ('name', 'language', 'release_date', 'genre', 'director')

# Shows these fields in the admin panel list view.

# search_fields = ('name', 'genre', 'director')

# Allows searching for movies by name, genre, or director in the admin panel.