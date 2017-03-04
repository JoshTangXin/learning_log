from django.shortcuts import render
from .models import Topic,Entry
from .forms import TopicForm , EntryForm
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout

# Create your views here.
def index(request):
	return render(request,'learning_logs/index.html')

# 需要从数据库中取出数据传给模板
# 装饰器 只有用户登录了才能进行下一步操作 否则重定向到登录界面  在setting.py中设置LOGIN_URL
@login_required
def topics(request):
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request,topic_id):
	topic = Topic.objects.get(id=topic_id)

	#复制root用户访问topic的url 即使是普通用户 使用这个url一样可以看到内容 我们需要加以限制
	if topic.owner != request.user:
		raise Http404
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)

# 如果是第一次进入这个界面 创建一个表单 否则处理数据 重定向到网页topics
# 模板中 {% csrf_token %} 放置跨站请求伪造
# {{ form.as_p }} 让Django自动创建显示表单所需的全部字段
@login_required
def new_topic(request):
	# 从服务器获取数据 GET 提交数据 POST
	if request.method != 'POST':
		#创建一个新的表单
		form = TopicForm()
	else:
		# request.POST包含提交的数据
		form = TopicForm(request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
		return HttpResponseRedirect(reverse('learning_logs:topics'))
	context={'form':form}
	return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request,topic_id):
	topic = Topic.objects.get(id=topic_id)

	if topic.owner != request.user:
		raise Http404

	if request.method != 'POST':
		form = EntryForm()
	else:
		form = EntryForm(request.POST)
		if form.is_valid():
			# commit=false 暂时先不保存到数据库中
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic_id]))

	context={'topic':topic, 'form':form}
	return render(request, 'learning_logs/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
	# 编辑已有的条目
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic

	if topic.owner != request.user:
		raise Http404
	if request.method != 'POST':
		# 初次请求 使用已有的条目填充
		form = EntryForm(instance=entry)
	else:
		form = EntryForm(instance=entry,data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)





