from django.http import Http404
from django.shortcuts import render, get_object_or_404
from polls.models import Poll

def index(request):
	latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
	context = { 'latest_poll_list': latest_poll_list }
	return render(request, 'polls/index.html', context)

def detail(request, poll_id):
	poll = get_object_or_404(Poll, pk = poll_id)
	return render(request, 'polls/detail.html', {'poll': poll})

def results(request):
	return HttpResponse("You are looking at the results for poll %s." % poll_id)

def vote(request):
	return HttpResponse("You are voting on poll %s." % poll_id)