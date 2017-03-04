from django.contrib import admin

# Register your models here.
from learning_logs.models import Topic,Entry

# 向管理网站注册自己的模型
admin.site.register(Topic)
admin.site.register(Entry)