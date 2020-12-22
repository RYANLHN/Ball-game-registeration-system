from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.user)
admin.site.register(models.matchlist)
admin.site.register(models.playerlist)
admin.site.register(models.fenzu)
admin.site.register(models.zhixuce)
admin.site.register(models.saichang)
admin.site.register(models.caipanall)
