from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.home, name="home"),
	path('register/', views.register,name='register'),
	path('user_login/', views.user_login,name='user_login'),
	path('logout/', views.user_logout,name='logout'),
	path('howitworks/', views.howitworks,name='howitworks'),
	path('contact/', views.contact,name='contact'),
	path('about/', views.about,name='about'),
	path('article/', views.article,name='article'),
	path('<int:id>/read_article/', views.read_article, name="read_article"),
	path('diabetes_risk/', views.diabetes_risk,name='diabetes_risk'),
	path('diabetes_risk_result/', views.diabetes_risk_result,name='diabetes_risk_result'),
	path('cvd_prediction/', views.cvd_prediction,name='cvd_prediction'),
	path('cvd_prediction_result/', views.cvd_prediction_result,name='cvd_prediction_result'),
	path('liver_diagnosis/', views.liver_diagnosis,name='liver_diagnosis'),
	path('liver_diagnosis_result/', views.liver_diagnosis_result,name='liver_diagnosis_result'),
	path('detect_brain_tumor/', views.detect_brain_tumor,name='detect_brain_tumor'),
	path('detect_brain_tumor_result/', views.detect_brain_tumor_result,name='detect_brain_tumor_result'),
	path('search/', views.search,name='search'),
	path('privacy/', views.privacy,name='privacy'),
	path('404/',views.page_not_found),

	path('reset_password/', auth_views.PasswordResetView.as_view(template_name='MAINAPP/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='MAINAPP/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='MAINAPP/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='MAINAPP/password_reset_complete.html'), name='password_reset_complete'),
]
