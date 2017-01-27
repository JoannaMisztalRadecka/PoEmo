from django.contrib import admin
from .models import Inspiration, Poem

admin.site.register(Poem)
admin.site.register(Inspiration)