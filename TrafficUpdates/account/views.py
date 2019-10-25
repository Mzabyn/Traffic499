from django.contrib.auth import(
	authenticate,
	get_user_model,
	login,
	logout,
	)
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_gravatar.helpers import get_gravatar_url, has_gravatar

from .models import UserInfo
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm

# Create your views here.

def login_view(request):
	# print(request.user.is_authenticated)
	if request.user.is_authenticated: #If the user is logged in already,then the post list is shown
		return redirect("home")
	form=UserLoginForm(request.POST or None)
	title="Login"
	loginPage=True;
	if form.is_valid():
		username=form.cleaned_data.get("username")				#Taking the fields for authentication
		password=form.cleaned_data.get("password")
		user = authenticate(username=username,password=password)
		login(request,user)
		return redirect("home")

	return render(request,"form.html",{"form":form, "title":title,"loginPage":loginPage})


def register_view(request):
	#print(request.user.is_authenticated())
	title="Register"
	form=UserRegistrationForm(request.POST or None)
	if form.is_valid():
		user=form.save(commit=False)
		password= form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		phone= form.cleaned_data.get('phone')
		userInfo= UserInfo.objects.create(user=user)
		userInfo.phone=phone
		userInfo.save()

		new_user= authenticate(username=user.username,password=password)
		login(request,new_user)	#User is logged in
		return redirect("home")

	context={
		"form":form,
		"title":title,
	}
	return render(request,"form.html",context)

@login_required(login_url='/login/')
def logout_view(request):
	logout(request)
	return redirect("login")

@login_required(login_url='/login/')
def profile(request):
	gravatar_exists = has_gravatar(request.user.email)
	instance= UserInfo.objects.filter(user=request.user).first()
	# print(gravatar_exists)
	# print(request.user.info.points)
	if instance.phone=="0":
		phoneAvailable= False
	else:
		phoneAvailable= True
	context={
		"exists":gravatar_exists,
		"instance": instance,
		"phone" : phoneAvailable,
	}
	return render(request,"profile.html",context)

@login_required(login_url='/login/')
def editProfile(request):
	#print(request.user.is_authenticated())
	title="Update"
	instance= UserInfo.objects.filter(user=request.user).first()
	if request.method == 'POST':
		number=request.POST.get('phoneNum')
		m= request.POST.get('showNum')
		n=len(number)
		if n == 11:
			instance.phone=number
			instance.save()
		if m == "Yes":
			instance.showPhone=True
			instance.save()
		else:
			instance.showPhone=False
			instance.save()
		print(m)
		u_form= UserUpdateForm(request.POST,instance=request.user)
		if u_form.is_valid():
			u_form.save()
			messages.success(request,"Your information has been updated successfully")
			return redirect("profile")
		else:
			messages.success(request,"Failed to update your information")
	else:
		u_form= UserUpdateForm(instance=request.user)

	context={
		"form":u_form,
		"title":title,
		"instance": instance,
	}
	return render(request,"profile_edit.html",context)

# def userList(request):
# 	queryset=User.objects.all().exclude(username=request.user.username).exclude(is_superuser=True)
# 	query=request.GET.get("q")				# Getting the value of the text box if search button is pressed
# 	if query:
# 		queryset=queryset.filter(last_name__icontains=query)	#User is searched with the last name
# 		if not queryset.exists():
# 			messages.success(request, "No search result found")
# 	context={
# 		"object_list": queryset,
# 		"title": "User List",
# 	}
# 	return render(request,"users.html",context)

@login_required(login_url='/login/')
def userProfile(request,id=None):
	instance=get_object_or_404(User,pk=id)
	if request.user==instance:
		return redirect("profile")
	gravatar_exists = has_gravatar(instance.email)
	instanceInfo= UserInfo.objects.filter(user=instance).first()
	print(gravatar_exists)
	context={
		"exists":gravatar_exists,
		"instance": instance,
		"instanceInfo": instanceInfo,
	}
	return render(request,"userProfile.html",context)
