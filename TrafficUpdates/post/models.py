from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
	creator = models.ForeignKey(User,default=1,on_delete=models.CASCADE) #default=1 to point the superuser
	content = models.TextField()
	post_time = models.DateTimeField(auto_now=False, auto_now_add=True) #automatically setting the posting time
	like_count= models.IntegerField(default=0)
	dislike_count= models.IntegerField(default=0)
	latitude=models.FloatField(default=0)
	longitude=models.FloatField(default=0)
	likers=models.ManyToManyField(User,related_name='likers')
	like_seen= models.BooleanField(default=True)
	dislikers=models.ManyToManyField(User,related_name='dislikers')
	dislike_seen= models.BooleanField(default=True)
	image= models.FileField(upload_to='post/',null=True,blank=True)
	def __str__(self):
		return self.content

	class Meta:
		ordering=['-post_time']   #For showing recent posts first


class Comment(models.Model):
	creator = models.ForeignKey(User,default=1,on_delete=models.CASCADE)
	post=models.ForeignKey(Post,on_delete=models.CASCADE)
	content = models.TextField()
	comment_time = models.DateTimeField(auto_now_add=True,auto_now=False)   #automatically setting the posting time
	like_count= models.IntegerField(default=0)
	dislike_count= models.IntegerField(default=0)
	seen= models.BooleanField(default=False)
	like_seen= models.BooleanField(default=True)
	commentLikers=models.ManyToManyField(User,related_name='commentLikers')
	dislike_seen= models.BooleanField(default=True)
	commentdisLikers=models.ManyToManyField(User,related_name='commentdisLikers')
	
	def __str__(self):
		return self.creator.last_name+'--'+self.content
