from django.db import models
from django.contrib.auth.models import User
from django.db.models import TextField
from django.utils import timezone

class Article(models.Model):
	posted_on=models.DateField(blank=True,default=timezone.now)
	posted_by =models.CharField(max_length=100,blank=True)
	article_name = models.CharField(max_length= 200)
	article_caption=models.TextField(blank=True)
	article_introduction=models.TextField(blank=True)
	article_sub_heading1 =models.CharField(max_length= 200 ,blank=True)
	article_sub_body1 =models.TextField(blank=True)
	article_conclusion =models.TextField(blank=True)
	article_image = models.ImageField(null=True, blank=True , help_text="crop image as square before upload to get uniform size in the page")
	add_article_to_home = models.BooleanField(default=False,null=True, blank=True ,help_text="Yes will enable to display it on home page")

	def __str__(self):
		return self.article_name

	@property
	def article_imageURL(self):
		try:
			url = self.article_image.url
		except:
			url = ''
		return url


class ContactMessage(models.Model):
	reviewer_name = models.CharField(max_length= 200 ,blank=True)
	reviewer_email=models.EmailField(max_length =200 ,blank=True)
	reviewer_message = models.TextField(max_length=5000,blank=True)

	def __str__(self):
		return self.reviewer_name

class DiagnosisTool(models.Model):
	tool_name = models.CharField(max_length= 200 ,blank=False)
	tool_accuracy = models.CharField(max_length= 200 ,blank=False)
	tool_technology = models.CharField(max_length= 200 ,blank=False)
	tool_detail = models.TextField(max_length=4000,blank=False)
	tool_link = models.CharField(max_length= 200 ,blank=False)
	def __str__(self):
		return self.tool_name

class Subscriber(models.Model):
	subscriber_name = models.CharField(max_length= 300 ,blank=True)
	subscriber_email=models.EmailField(max_length =300 ,blank=True)
	def __str__(self):
		return self.subscriber_name
