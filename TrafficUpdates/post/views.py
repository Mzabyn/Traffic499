from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .forms import PostForm, CommentForm
from account.models import UserInfo
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

@login_required(login_url='/login/')
def posts(request):
	if request.method == 'POST' and request.is_ajax():
		print("Yo")
		m= request.POST.get('location1')
		print(m)
		request.session['lat']=m
		n= request.POST.get('location2')
		print(n)
		request.session['long']=n
		return JsonResponse({
                'success': True,
                # 'url': 'my_ajax_request',
            })  
	
	time_threshold = timezone.now() - timedelta(hours=2)
	deleteOldPosts = Post.objects.filter(post_time__lt=time_threshold)
	# print(deleteOldPosts)	
	# if deleteOldPosts.exists():
	# 	deleteOldPosts.delete()
	# 	print(Post.objects.all())
	for post in deleteOldPosts:
		if post.image:
			post.image.delete()
		post.delete()
	print(Post.objects.all())
	user=UserInfo.objects.filter(user=request.user).first()
	x=User.objects.count()
	print(x)
	notification=False
	unseen_likePost= Post.objects.filter(creator=request.user).filter(like_seen=False)
	unseen_dislikePost= Post.objects.filter(creator=request.user).filter(dislike_seen=False)
	unseen_likeComment= Comment.objects.filter(creator=request.user).filter(like_seen=False)
	unseen_dislikeComment= Comment.objects.filter(creator=request.user).filter(dislike_seen=False)
	unread_comments=Comment.objects.all().filter(seen=False) # Comments not seen
	posts1=Post.objects.all().filter(pk__in=[comment.post.id for comment in unread_comments]).filter(creator=request.user)
	if unseen_dislikeComment or unseen_likeComment or unseen_dislikePost or unseen_likePost or posts1:
		notification=True
	# if user.points >= 1000 and user.points < 2000:
	# 	user.level=2
	# elif user.points >= 2000 and user.points < 3000:
	# 	user.level=3
	# elif user.points >= 3000 and user.points < 4000:
	# 	user.level=4
	# elif user.points >= 4000:
	# 	user.level=5
	k= 10 + ((100*x)/45)
	if user.level == 1 and user.points > (k*30):
		# print("Yo1")
		user.level=2
		messages.success(request, "Congrats! You have reached reliability level 2")
	elif user.level == 2 and user.points > (k*180):
		# print("Yo2")
		user.level=3
		messages.success(request, "Congrats! You have reached reliability level 3")
	elif user.level == 3 and user.points > (k*360):
		# print("Yo3")
		user.level=4
		messages.success(request, "Congrats! You have reached reliability level 4")
	elif user.level == 4 and user.points > (k*720):
		# print("Yo4")
		user.level=5
		messages.success(request, "Congrats! You have reached reliability level 5")
	user.save()
	context={
	"title": "Real-time Traffic Update",
	"notification": notification
	}
	return render(request,"map.html",context)

@login_required(login_url='/login/')
def create_post(request):
	if not request.user.is_authenticated:
		raise Http404
	lat= request.session['lat']
	lon= request.session['long']
	form=PostForm(request.POST or None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.creator=request.user
		instance.latitude= lat
		instance.longitude= lon
		if request.FILES:
			n=request.FILES['fileUp']
			instance.image=n
			print("In files req")
		#print(instance.creator)
		print("Yo")
		print(instance.image.name)
		print("Yo")
		instance.save()
		user=UserInfo.objects.filter(user=request.user).first()
		user.points=user.points+10
		user.save()
		messages.success(request, "You have gained 10 points!")
		return redirect("create")    #Going to home after creating the post successfully
	lonf= float(lon)
	latf= float(lat)
	lonup= lonf + 0.01
	lonlow= lonf - 0.01
	latup= latf + 0.01
	latlow= latf - 0.01
	queryset=Post.objects.filter(latitude__gte=latlow,latitude__lte=latup).filter(longitude__gte=lonlow,longitude__lte=lonup)
	print(queryset)
	context={
		"title": "Create Post",
		"form":form,
		"objects": queryset,
	}
	return render(request,"post_form.html",context)

@login_required(login_url='/login/')
def delete_post(request,id=None):
	instance=get_object_or_404(Post,pk=id)
	context={
		"instance":instance,
	}
	if request.method=="POST":
		if request.user==instance.creator:
			if instance.image:
				instance.image.delete()
			instance.delete()								
			messages.success(request, "Successfully Deleted")		#User is notified if the post is deleted
		else:
			messages.success(request, "You didn't post this")
		return redirect("create") #After deleting a post user is taken to the homepage
	return render(request,"confirmation.html",context)
	# if request.user==instance.creator:
	# 	instance.delete()
	# return redirect("create")

@login_required(login_url='/login/')
def like_post(request,id=None):
	instance=get_object_or_404(Post,pk=id)
	if not request.user==instance.creator:
		if not request.user in instance.likers.all():
			print(instance.likers.all())
			user=UserInfo.objects.filter(user=instance.creator).first()
			user.points=user.points+100
			user.save()
			print(user.points)
			instance.like_count=instance.like_count+1
			instance.likers.add(request.user)
			instance.like_seen=False
			instance.save()
		else:
			print("Already liked")
			messages.success(request, "You already liked this post.")
	else:
		messages.success(request, "You can't like your own post.")
	return redirect("create")

@login_required(login_url='/login/')
def dislike_post(request,id=None):
	instance=get_object_or_404(Post,pk=id)
	if not request.user==instance.creator:
		if not request.user in instance.dislikers.all():
			user=UserInfo.objects.filter(user=instance.creator).first()
			user.points=user.points-10
			user.save()
			instance.dislike_count=instance.dislike_count+1
			instance.dislikers.add(request.user)
			instance.dislike_seen=False
			instance.save()
		else:
			print("Already disliked")
			messages.success(request, "You already disliked this post.")
	else:
		messages.success(request, "You can't dislike your own post.")
	return redirect("create")

@login_required(login_url='/login/')
def like_comment(request,cid=None,id=None):
	instance=get_object_or_404(Comment,pk=cid)
	if not request.user==instance.creator:
		if not request.user in instance.commentLikers.all():
			user=UserInfo.objects.filter(user=instance.creator).first()
			user.points=user.points+50
			user.save()
			instance.like_count=instance.like_count+1
			instance.commentLikers.add(request.user)
			instance.like_seen=False
			instance.save()
		else:
			messages.success(request, "You already liked this comment.")
	else:
		messages.success(request, "You can't like your own comment.")
	return redirect("details",id)

@login_required(login_url='/login/')
def dislike_comment(request,cid=None,id=None):
	instance=get_object_or_404(Comment,pk=cid)
	if not request.user==instance.creator:
		if not request.user in instance.commentdisLikers.all():
			user=UserInfo.objects.filter(user=instance.creator).first()
			user.points=user.points-10
			user.save()
			instance.dislike_count=instance.dislike_count+1
			instance.commentdisLikers.add(request.user)
			instance.dislike_seen=False
			instance.save()
		else:
			messages.success(request, "You already disliked this comment.")
	else:
		messages.success(request, "You can't dislike your own comment.")
	return redirect("details",id)

@login_required(login_url='/login/')
def notification(request):
	unseen_likePost= Post.objects.filter(creator=request.user).filter(like_seen=False)
	unseen_dislikePost= Post.objects.filter(creator=request.user).filter(dislike_seen=False)
	unseen_likeComment= Comment.objects.filter(creator=request.user).filter(like_seen=False)
	unseen_dislikeComment= Comment.objects.filter(creator=request.user).filter(dislike_seen=False)
	unread_comments=Comment.objects.all().filter(seen=False) # Comments not seen
	posts=Post.objects.all().filter(pk__in=[comment.post.id for comment in unread_comments]).filter(creator=request.user)
	if request.GET.get('Clear') == 'Clear':
		for post in unseen_likePost:
			post.like_seen=True
			post.save()
		for comment in unseen_likeComment:
			comment.like_seen=True
			comment.save()
		for post1 in unseen_dislikePost:
			post1.dislike_seen=True
			post1.save()
		for comment1 in unseen_dislikeComment:
			comment1.dislike_seen=True
			comment1.save()
		for postComment in posts:
			for comments in postComment.comment_set.all():
				comments.seen=True
				comments.save()
			postComment.save()
		return redirect('notification')
	context={
		"posts": unseen_likePost,
		"comments": unseen_likeComment,
		"posts1": unseen_dislikePost,
		"comments1": unseen_dislikeComment,
		"commentPost": posts,
	}
	return render(request,"notification.html",context);

@login_required(login_url='/login/')
def post_details(request,id=None):
	instance=get_object_or_404(Post,pk=id)

	if request.user==instance.creator:
		for comment in instance.comment_set.all():
			comment.seen=True
			comment.save()

	comment_form=CommentForm(request.POST or None)
	if comment_form.is_valid():
		comment_instance=comment_form.save(commit=False)
		comment_instance.creator=request.user
		comment_instance.post=instance       #assigning the post of the comment
		if request.user==instance.creator:
			comment_instance.seen=True
		comment_instance.save()
		comment_form=CommentForm() # to clear the form after comment is posted
	context={
		"object": instance,
		"form": comment_form,
	}

	return render(request,"post_details.html",context)

@login_required(login_url='/login/')
def delete_comment(request,cid=None,id=None): #Here id argument is passed for redirecting to the details page
	instance=get_object_or_404(Comment,pk=cid)
	if isinstance(instance,Comment):
		isComment= True
	else:
		isComment=False
	context={
		"instance":instance,
		"isComment":isComment,
	}
	if request.method=="POST":
		if request.user==instance.creator or request.user==instance.post.creator:
			instance.delete()
			messages.success(request, "Successfully Deleted")		#User is notified if the comment is deleted
		else:
			messages.success(request, "You didn't comment this")
		return redirect("details",id) #Here the id passed is the post id needed for post details url
	return render(request,"confirmation.html",context)

@login_required(login_url='/login/')
def sendMail(request,id=None):
	query=request.GET.get("q")
	if query:
		email_to=[query]
		subject = 'Real-time Dhaka'
		message = 'Hey! This website Real-Time Dhaka shows you the traffic in Dhaka and informs you of the circumstances that may cause traffic, as soon as they happen! It has saved me so much time AND it is free! Check it out at: www.realtimedhaka.com '
		email_from = settings.EMAIL_HOST_USER	
		send_mail(subject,message,email_from,email_to)
		user=UserInfo.objects.filter(user=request.user).first()
		user.points=user.points+20
		user.save()
		messages.success(request, "You have gained 20 points!")
	if request.method == 'POST':
		emailTo=request.POST.get('email')
		email_to=[emailTo]
		subject = 'Real-time Dhaka'
		message = request.POST.get('msg')
		email_from = settings.EMAIL_HOST_USER	
		send_mail(subject,message,email_from,email_to)
		user=UserInfo.objects.filter(user=request.user).first()
		user.points=user.points+20
		user.save()
		messages.success(request, "You have gained 20 points!")
	context={
		"title":"Invite",
	}
	return render(request,"invite.html",context)

class postList(APIView):
	def get(self,request):
		posts=Post.objects.all()
		serializers=PostSerializer(posts, many=True)
		return Response(serializers.data)