from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# MVC中的M 对应到数据库中就是数据表
# Field的类型决定在数据库中的类型 在前端的显示 以及 做简单的验证
# 代码层面上 模型就是一个类

class Topic(models.Model):
	text = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)
	# 将数据关联到提交他的用户
	owner = models.ForeignKey(User)

	def __str__(self):
		return self.text

# 为添加的Chess 以及 Rock Climbing添加模型 他们和Topic是多对一的关系 用Foreign key
class Entry(models.Model):
	topic=models.ForeignKey(Topic)
	text = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)

	# Meta是一个内部类 其中verbose_name_plural指定了模型的复数形式 不指定默认在后面加s
	class Meta:
		verbose_name_plural = 'entries'

	def __str__(self):
		if len(self.text) > 50 :
			return self.text[:50] + '...'
		else:
			return self.text
