from django import forms
from .models import Topic,Entry

# 之前添加数据都是超级用户通过管理界面添加的  现在 创建一个方便普通用户输入数据的表单
# 创建表单最简单就是使用Django ModelForm
class TopicForm(forms.ModelForm):
	class Meta:
		'''选择根据哪个模型来创建表单'''
		model=Topic
		'''表单只包含一个text字段'''
		fields=['text']
		'''不要为text字段生成标签'''
		labels={'text':''}


class EntryForm(forms.ModelForm):
	class Meta:
		model = Entry
		fields = ['text']
		labels = {'text': ''}
		# widgets HTML元素 允许为text字段定义默认输入部件
		widgets = {'text':forms.Textarea(attrs={'cols':80})}