from django.contrib import admin

from .models import *


# Register your models here.
admin.site.register(Team)
admin.site.register(Question)
admin.site.register(TestCase)
admin.site.register(TestCaseTry)
admin.site.register(Setting)
