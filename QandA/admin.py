from django.contrib import admin

# Register your models here.

from .models import Tag, Question, QComment, Faculty, Department

admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(QComment)
admin.site.register(Faculty)
admin.site.register(Department)