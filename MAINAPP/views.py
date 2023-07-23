from django.shortcuts import render
from . import forms
from .models import *
from MAINAPP.forms import UserForm, ContactMessageForm, SubscriberForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect , HttpResponse
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import joblib
import numpy as np


RFClassifierDiabetes=joblib.load('RFClassifierDiabetes.pkl')
RFRegressorDiabetes=joblib.load('RFRegressorDiabetes.pkl')
RFCHeart=joblib.load('RFCHeartModel.pkl')
RFRHeart=joblib.load('RFRHeartModel.pkl')
RFCBrainTumor=joblib.load('RFCBrainTumor.pkl')
RFRBrainTumor=joblib.load('RFRBrainTumor.pkl')
GBClassifierLiver=joblib.load('GBClassifierLiver.pkl')
GBRegressorLiver=joblib.load('GBRegressorLiver.pkl')

# Create your views here.
def home(request):
	subscribe_form = forms.SubscriberForm()
	if request.method =='POST':
		subscribe_form = forms.SubscriberForm(request.POST)
		to = request.POST['subscriber_email']
		subject = 'The Heartbeat'
		body = 'Welcome'+'<p style="font-size:13px;">Thank you for subscribing to The HeartBeat, we are glad to welcome you. The Heartbeat is your intelligent diagnostic expert integrated with widely used machine learning models with up-to 90% of accuracy. We offer variety of tools to predict the presence of diabetes, cardiovascular disease , Brain Tumour & more. Get your hands on our free tools now.</p>'+'<p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The HeartBeat Team</b></p>'
		msg = EmailMultiAlternatives(subject, body,'mrinalmayank7@gmail.com', [to])
		msg.content_subtype = "html"
		msg.send(fail_silently=False)

		if subscribe_form.is_valid():
			subscribe_form.save()
			messages.info(request,"Successfully subscribed")
			return HttpResponseRedirect(reverse('home'))
		else:
			messages.error(request,"Invalid Details")
			return HttpResponseRedirect(reverse('home'))
	pages = Article.objects.all()
	context = {'pages':pages ,'subscribe_form':subscribe_form}
	return render(request, 'MAINAPP/home.html', context)

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))


def register(request):
	registered = False
	if request.method =='POST':
		user_form =UserForm(data = request.POST)

		if user_form.is_valid():
			 user =user_form.save()
			 user.set_password(user.password)
			 user.save()

			 registered = True
			 messages.info(request,"Successfully Registered")
		else:
			print(user_form.errors)
	else :
		user_form =UserForm
	return render(request ,'MAINAPP/register.html',{'user_form': user_form ,'registered' : registered })



def user_login(request):
	if request.method =='POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username , password=password )
		if user:
			if user.is_active:
				login(request , user)
				return HttpResponseRedirect(reverse('home'))

			else:
				return HttpResponse("ACCOUNT NOT ACTIVE")
		else:
			messages.error(request,"Invalid login details.")
			return HttpResponseRedirect("/user_login")
	else:
		return render(request , 'MAINAPP/login.html',{})

def article(request):

	pages = Article.objects.all()
	topics =reversed(Article.objects.all().order_by('id'))
	context = {'pages':pages ,'topics':topics}
	return render(request, 'MAINAPP/article.html', context)

def read_article(request ,id):
	page = Article.objects.get(id=id)
	topics =reversed(Article.objects.all().order_by('id'))
	context = {'page':page ,'topics':topics}
	return render(request, 'MAINAPP/read_article.html', context)

def diabetes_risk(request):
	return render(request, 'MAINAPP/diabetes.html')

def diabetes_risk_result(request):
	if request.method == 'POST':
		Pregnancies=request.POST.get('val1')
		Glucose=request.POST.get('val2')
		BloodPressure=request.POST.get('val3')
		SkinThickness=request.POST.get('val4')
		Insulin=request.POST.get('val5')
		BMI=request.POST.get('val6')
		DiabetesPedigreeFunction=request.POST.get('val7')
		Age=request.POST.get('val8')
	input_data = (Pregnancies ,Glucose ,BloodPressure,SkinThickness ,Insulin ,BMI ,DiabetesPedigreeFunction ,Age)
	input_data_as_numpy_array= np.asarray(input_data)
	input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
	PredictModelRFC = RFClassifierDiabetes.predict(input_data_reshaped)
	PredictModelRFR= RFRegressorDiabetes.predict(input_data_reshaped)*100
	if request.user.is_authenticated :
		userfirstname=request.user.first_name
		risk=str(PredictModelRFR[0])
		if PredictModelRFC[0]==0:
			outcome="Lower chances of diabetes."
		else:
			outcome="Higher risk of diabetes, consult your local medical authority for advice."

		to = request.user.email
		subject = 'The Heartbeat'
		body = 'Hello '+userfirstname+'<p style="font-size:13px;"><b>Thank you for trusting our services, we are sending this email to let you know about the predicted outcomes on the basis of measures provided by you. For any queries drop us a mail at mrinalmayank7@gmail.com</b></p>'+'<p style="font-size:15px;"><b>Measures provided by you :</b></p>'+'Pregnancies. &nbsp;&nbsp;'+Pregnancies+'<br>'+'Glucose. &nbsp;&nbsp;'+Glucose+'<br>'+'Blood Pressure. &nbsp;&nbsp;'+BloodPressure+'<br>'+'Skin Thickness. &nbsp;&nbsp;'+SkinThickness+'<br>'+'Insulin. &nbsp;&nbsp;'+Insulin+'<br>'+'BMI. &nbsp;&nbsp;'+BMI+'<br>'+'Diabetes pedigree func. &nbsp;&nbsp;'+DiabetesPedigreeFunction+'<br>'+'Age. &nbsp;&nbsp;'+Age+'<br>'+'<p style="font-size:18px;text-align:center"><b>Outcomes</b></p>'+'<b>Diabetes Risk</b> &nbsp;&nbsp; '+risk+' % <br>'+'<b>Remarks. &nbsp;&nbsp;</b>'+outcome+'<hr><p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The HeartBeat Team</b></p>'+'<p style="font-size:13px;color:#A6ACAF;text-align:center;"><i>These outcomes are for informational purposes only, Consult your local medical authority for advice.</i></p>'
		msg = EmailMultiAlternatives(subject, body,'mrinalmayank7@gmail.com', [to])
		msg.content_subtype = "html"
		msg.send(fail_silently=False)

	context={'output1':PredictModelRFR[0] ,'output2':PredictModelRFC[0] ,'p':Pregnancies,'g':Glucose,'bp':BloodPressure,'st':SkinThickness,'insulin':Insulin,'bmi':BMI,'dpf':DiabetesPedigreeFunction,'age':Age}
	return render(request, 'MAINAPP/diabetes.html',context)

def cvd_prediction(request):
	context = {}
	return render(request, 'MAINAPP/heart.html', context)

def cvd_prediction_result(request):
	if request.method == 'POST':
		age=request.POST.get('val1')
		sex=request.POST.get('val2')
		cp=request.POST.get('val3')
		trestbps=request.POST.get('val4')
		chol=request.POST.get('val5')
		fbs=request.POST.get('val6')
		restecg=request.POST.get('val7')
		thalach=request.POST.get('val8')
		exang=request.POST.get('val9')
		oldpeak=request.POST.get('val10')
		slope=request.POST.get('val11')
	input_data = (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope)
	input_data_as_numpy_array= np.asarray(input_data)
	input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
	PredictRFCHeart= RFCHeart.predict(input_data_reshaped)
	PredictRFRHeart= RFRHeart.predict(input_data_reshaped)*100
	if sex== '1':
		genderText="Male"
	else:
		genderText="Female"

	if fbs== '1':
		fbsText="Yes"
	else:
		fbsText="No"

	if cp== '3':
		cpText="Typical angina"
	elif cp=='2':
		cpText="Non-anginal pain"
	elif cp=='1':
		cpText='Atypical angina'
	else:
		cpText='Asymptomatic'

	if restecg=='2':
		restecgText="Having ST-T wave abnormality"
	elif restecg=='1':
		restecgText="Normal"
	else:
		restecgText="Probable/definite left ventricular hypertrophy"

	if exang=='1':
		exangText ="Yes"
	else:
		exangText ="No"

	if slope=='2':
		slopeText="Upsloping"
	elif slope=='1':
		slopeText="Flat"
	else:
		slopeText="Downsloping"

	if request.user.is_authenticated :
		userfirstname=request.user.first_name
		risk=str(PredictRFRHeart[0])
		if PredictRFCHeart[0]==0:
			outcome="Lower possibility of  cardiovascular disease"
		else:
			outcome="Higher risk of cardiovascular disease, consult your local medical authority for advice."

		to = request.user.email
		subject = 'The Heartbeat'
		body = 'Hello '+userfirstname+'<p style="font-size:13px;"><b>Thank you for trusting our services, we are sending this email to let you know about the predicted outcomes on the basis of measures provided by you. For any queries drop us a mail at mrinalmayank7@gmail.com</b></p>'+'<p style="font-size:15px;"><b>Measures provided by you :</b></p>'+'Age. &nbsp;&nbsp;'+age+'<br>'+'Resting blood pressure. &nbsp;&nbsp;'+trestbps+'<br>'+'Cholesterol. &nbsp;&nbsp;'+chol+'<br>'+'Thalach. &nbsp;&nbsp;'+thalach+'<br>'+'Oldpeak. &nbsp;&nbsp;'+oldpeak+'<br>'+'Gender. &nbsp;&nbsp;'+genderText+'<br>'+'Fasting blood sugar > 120 mg/dl. &nbsp;&nbsp;'+fbsText+'<br>'+'Chest pain type. &nbsp;&nbsp;'+cpText+'<br>'+'Resting electrocardiographic results. &nbsp;&nbsp;'+restecgText+'<br>'+'Exercise induced angina. &nbsp;&nbsp;'+exangText+'<br>'+'Slope of the peak exercise ST segment. &nbsp;&nbsp;'+slopeText+'<br>'+'<p style="font-size:18px;text-align:center"><b>Outcomes</b></p>'+'<b>CVD Risk </b> &nbsp;&nbsp; '+risk+' % <br>'+'<b>Remarks. &nbsp;&nbsp;</b>'+outcome+'<hr><p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The HeartBeat Team</b></p>'+'<p style="font-size:13px;color:#A6ACAF;text-align:center;"><i>These outcomes are for informational purposes only, Consult your local medical authority for advice.</i></p>'
		msg = EmailMultiAlternatives(subject, body,'mrinalmayank7@gmail.com', [to])
		msg.content_subtype = "html"
		msg.send(fail_silently=False)
	context={'output1':PredictRFRHeart[0] ,'output2':PredictRFCHeart[0] ,'age':age, 'sex':sex, 'cp':cp, 'tb':trestbps, 'cl':chol, 'fb':fbs, 'rst':restecg, 'thal':thalach, 'ex':exang, 'old':oldpeak, 'slp':slope, 'genderText':genderText,'fbsText':fbsText,'cpText':cpText,'restecgText':restecgText,'exangText':exangText,'slopeText':slopeText}
	return render(request, 'MAINAPP/heart.html', context)

def liver_diagnosis(request):
	context = {}
	return render(request, 'MAINAPP/liver.html', context)

def liver_diagnosis_result(request):
	if request.method == 'POST':
		Age=request.POST.get('val1')
		Gender=request.POST.get('val2')
		Total_Bilirubin=request.POST.get('val3')
		Direct_Bilirubin=request.POST.get('val4')
		Alkaline_Phosphotase=request.POST.get('val5')
		Alamine_Aminotransferase=request.POST.get('val6')
		Aspartate_Aminotransferase=request.POST.get('val7')
		Total_Protiens=request.POST.get('val8')
		Albumin=request.POST.get('val9')
		Albumin_and_Globulin_Ratio=request.POST.get('val10')
	input_data = (Age, Gender, Total_Bilirubin, Direct_Bilirubin, Alkaline_Phosphotase, Alamine_Aminotransferase, Aspartate_Aminotransferase, Total_Protiens, Albumin, Albumin_and_Globulin_Ratio)
	input_data_as_numpy_array= np.asarray(input_data)
	input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
	PredictGBClassifierLiver = GBClassifierLiver.predict(input_data_reshaped)
	PredictGBRegressorLiver= GBRegressorLiver.predict(input_data_reshaped)*100
	if Gender== '1':
		GenderText="Male"
	else:
		GenderText="Female"

	if request.user.is_authenticated :
		userfirstname=request.user.first_name
		risk=str(PredictGBRegressorLiver[0])
		if PredictGBClassifierLiver[0]==0:
			outcome="Lower possibility of  liver disease"
		else:
			outcome="Higher risk of liver disease, consult your local medical authority for advice."

		to = request.user.email
		subject = 'The Heartbeat'
		body = 'Hello '+userfirstname+'<p style="font-size:13px;"><b>Thank you for trusting our services, we are sending this email to let you know about the predicted outcomes on the basis of measures provided by you. For any queries drop us a mail at mrinalmayank7@gmail.com</b></p>'+'<p style="font-size:15px;"><b>Measures provided by you :</b></p>'+'Age. &nbsp;&nbsp;'+Age+'<br>'+'Gender. &nbsp;&nbsp;'+GenderText+'<br>'+'Total Bilirubin. &nbsp;&nbsp;'+Total_Bilirubin+'<br>'+'Direct Bilirubin. &nbsp;&nbsp;'+Direct_Bilirubin+'<br>'+'Alkaline Phosphotase. &nbsp;&nbsp;'+Alkaline_Phosphotase+'<br>'+'Alamine Aminotransferase. &nbsp;&nbsp;'+Alamine_Aminotransferase+'<br>'+'Aspartate Aminotransferase. &nbsp;&nbsp;'+Aspartate_Aminotransferase+'<br>'+'Total Protiens. &nbsp;&nbsp;'+Total_Protiens+'<br>'+'Albumin. &nbsp;&nbsp;'+Albumin+'<br>'+'Albumin and Globulin Ratio. &nbsp;&nbsp;'+Albumin_and_Globulin_Ratio+'<br>'+'<p style="font-size:18px;text-align:center"><b>Outcomes</b></p>'+'<b>Risk </b> &nbsp;&nbsp; '+risk+' % <br>'+'<b>Remarks. &nbsp;&nbsp;</b>'+outcome+'<hr><p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The HeartBeat Team</b></p>'+'<p style="font-size:13px;color:#A6ACAF;text-align:center;"><i>These outcomes are for informational purposes only, Consult your local medical authority for advice.</i></p>'
		msg = EmailMultiAlternatives(subject, body,'mrinalmayank7@gmail.com', [to])
		msg.content_subtype = "html"
		msg.send(fail_silently=False)
	context={'output1':PredictGBRegressorLiver[0] ,'output2':PredictGBClassifierLiver[0] ,'Age':Age, 'Gender':Gender, 'TBIL':Total_Bilirubin,'DBIL':Direct_Bilirubin, 'ALKP':Alkaline_Phosphotase, 'Alamine':Alamine_Aminotransferase, 'Aspartate':Aspartate_Aminotransferase, 'Protiens':Total_Protiens, 'Albumin':Albumin, 'AGR':Albumin_and_Globulin_Ratio,'GenderText':GenderText}
	return render(request, 'MAINAPP/liver.html', context)

def detect_brain_tumor(request):
	context = {}
	return render(request, 'MAINAPP/brain.html', context)

def detect_brain_tumor_result(request):
	if request.method == 'POST':
		Mean=request.POST.get('val1')
		Variance=request.POST.get('val2')
		StandardDeviation=request.POST.get('val3')
		Entropy=request.POST.get('val4')
		Skewness=request.POST.get('val5')
		Kurtosis=request.POST.get('val6')
		Contrast=request.POST.get('val7')
		Energy=request.POST.get('val8')
		ASM	=request.POST.get('val9')
		Homogeneity=request.POST.get('val10')
		Dissimilarity=request.POST.get('val11')
		Correlation=request.POST.get('val12')
		Coarseness=request.POST.get('val13')
		PSNR=request.POST.get('val14')
		SSIM=request.POST.get('val15')
		MSE=request.POST.get('val16')
		DC=request.POST.get('val17')
	input_data = (Mean, Variance, StandardDeviation, Entropy, Skewness, Kurtosis, Contrast, Energy, ASM, Homogeneity, Dissimilarity, Correlation, Coarseness, PSNR, SSIM, MSE, DC)
	input_data_as_numpy_array= np.asarray(input_data)
	input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
	PredictRFCBrainTumor= RFCBrainTumor.predict(input_data_reshaped)
	PredictRFRBrainTumor= RFRBrainTumor.predict(input_data_reshaped)*100
	if request.user.is_authenticated :
		userfirstname=request.user.first_name
		risk=str(PredictRFRBrainTumor[0])
		if PredictRFCBrainTumor[0]==0:
			outcome="Possibility of brain tumour is negligible."
		else:
			outcome="Higher possibility of brain tumour detected."

		to = request.user.email
		subject = 'The Heartbeat'
		body = 'Hello '+userfirstname+'<p style="font-size:13px;"><b>Thank you for trusting our services, we are sending this email to let you know about the predicted outcomes on the basis of measures provided by you. For any queries drop us a mail at mrinalmayank7@gmail.com</b></p>'+'<p style="font-size:15px;"><b>Measures provided by you :</b></p>'+'Mean. &nbsp;&nbsp;'+Mean+'<br>'+'Variance. &nbsp;&nbsp;'+Variance+'<br>'+'Standard Deviation. &nbsp;&nbsp;'+StandardDeviation+'<br>'+'Entropy. &nbsp;&nbsp;'+Entropy+'<br>'+'Skewness. &nbsp;&nbsp;'+Skewness	+'<br>'+'Kurtosis. &nbsp;&nbsp;'+Kurtosis+'<br>'+'Contrast. &nbsp;&nbsp;'+Contrast+'<br>'+'Energy. &nbsp;&nbsp;'+Energy+'<br>'+'ASM. &nbsp;&nbsp;'+ASM+'<br>'+'Homogeneity. &nbsp;&nbsp;'+Homogeneity+'<br>'+'Dissimilarity. &nbsp;&nbsp;'+Dissimilarity+'<br>'+'Correlation. &nbsp;&nbsp;'+Correlation+'<br>'+'Coarseness. &nbsp;&nbsp;'+Coarseness+'<br>'+'PSNR. &nbsp;&nbsp;'+PSNR+'<br>'+'SSIM. &nbsp;&nbsp;'+SSIM+'<br>'+'MSE. &nbsp;&nbsp;'+MSE+'<br>'+'DC. &nbsp;&nbsp;'+DC+'<br>'+'<p style="font-size:18px;text-align:center"><b>Outcomes</b></p>'+'<b>Possibility. </b> &nbsp;&nbsp; '+risk+' % <br>'+'<b>Remarks. &nbsp;&nbsp;</b>'+outcome+'<hr><p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The HeartBeat Team</b></p>'+'<p style="font-size:13px;color:#A6ACAF;text-align:center;"><i>These outcomes are for informational purposes only, Consult your local medical authority for advice.</i></p>'
		msg = EmailMultiAlternatives(subject, body,'mrinalmayank7@gmail.com', [to])
		msg.content_subtype = "html"
		msg.send(fail_silently=False)
	context={'output1':PredictRFRBrainTumor[0] ,'output2':PredictRFCBrainTumor[0] ,'Mean':Mean, 'Variance':Variance, 'StandardDeviation':StandardDeviation, 'Entropy':Entropy, 'Skewness':Skewness, 'Kurtosis':Kurtosis,'Contrast': Contrast, 'Energy':Energy, 'ASM':ASM, 'Homogeneity':Homogeneity, 'Dissimilarity':Dissimilarity, 'Correlation':Correlation, 'Coarseness':Coarseness, 'PSNR':PSNR, 'SSIM':SSIM, 'MSE':MSE, 'DC':DC}
	return render(request, 'MAINAPP/brain.html', context)

def contact(request):
	ct_form = forms.ContactMessageForm()
	if request.method =='POST':
		ct_form = forms.ContactMessageForm(request.POST)
		to = request.POST['reviewer_email']
		subject = 'The Heartbeat'
		body = 'Hello'+'<p style="font-size:12px;">Thank you for reaching us, your message has been receieved & We will contact you shortly.</p>'+'<p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The HeartBeat Team</b></p>'
		msg = EmailMultiAlternatives(subject, body,'mrinalmayank7@gmail.com', [to])
		msg.content_subtype = "html"
		msg.send(fail_silently=False)


		if ct_form.is_valid():
			ct_form.save()
			messages.info(request,"Successfully submitted !")
			return HttpResponseRedirect(reverse('contact'))
		else:
			messages.error(request,"Invalid Details")
			return HttpResponseRedirect("/contact")
	context = {'ct_form':ct_form}
	return render(request, 'MAINAPP/contact.html', context)

def howitworks(request):
	context = {}
	return render(request, 'MAINAPP/howitworks.html', context)

def about(request):
	context = {}
	return render(request, 'MAINAPP/about.html', context)
def privacy(request):
	context = {}
	return render(request, 'MAINAPP/privacy.html', context)

def search(request):
	query=request.GET['query']
	pages_posted_on = Article.objects.filter(posted_on__icontains=query)
	pages_posted_by = Article.objects.filter(posted_by__icontains=query)
	pages_article_name = Article.objects.filter(article_name__icontains=query)
	pages_article_caption = Article.objects.filter(article_caption__icontains=query)
	pages_article_introduction = Article.objects.filter(article_introduction__icontains=query)
	pages_article_sub_heading1 = Article.objects.filter(article_sub_heading1__icontains=query)
	pages_article_sub_body1 = Article.objects.filter(article_sub_body1__icontains=query)
	pages_article_conclusion = Article.objects.filter(article_conclusion__icontains=query)
	pages =pages_posted_on.union(pages_posted_by, pages_article_name, pages_article_caption, pages_article_introduction, pages_article_sub_heading1, pages_article_sub_body1, pages_article_conclusion)

	tools_tool_name = DiagnosisTool.objects.filter(tool_name__icontains=query)
	tools_tool_accuracy = DiagnosisTool.objects.filter(tool_accuracy__icontains=query)
	tools_tool_technology = DiagnosisTool.objects.filter(tool_technology__icontains=query)
	tools_tool_detail = DiagnosisTool.objects.filter(tool_detail__icontains=query)
	tools=tools_tool_name.union(tools_tool_accuracy,tools_tool_technology,tools_tool_detail )
	context = {'tools':tools ,'pages':pages ,'query':query }
	return render(request, 'MAINAPP/search.html', context)

def  page_not_found(request ,exception=None):
	return render(request, 'MAINAPP/404.html')
