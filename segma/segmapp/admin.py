from django.contrib import admin
from segmapp import models
# Register your models here.
admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Relation)
admin.site.register(models.Request)
admin.site.register(models.Bio)
