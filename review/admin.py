from django.contrib import admin

# Register your models here.
from .models import Semester, Day, Period, Review, Comment

admin.site.register(Semester)
admin.site.register(Day)
admin.site.register(Period)
admin.site.register(Review)
admin.site.register(Comment)