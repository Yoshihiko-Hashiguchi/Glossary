from django.contrib import admin
from .models import Terms, Comments, Replys

# Register your models here.
admin.site.register(Terms)
admin.site.register(Comments)
admin.site.register(Replys)