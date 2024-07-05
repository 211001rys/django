from django.shortcuts import render
from django.urls import path
from . import views
from .views import login_view
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
# 管理者
    path('home1', views.home1, name='home1'),
    path('register/', views.employee_register, name='employee_register'),
    path('confirm/', views.employee_confirm, name='employee_confirm'),
    path('complete/', views.employee_register_complete, name='employee_register_complete'),
    path('employee/search/', views.employee_search_view, name='employee_search_view'),
    path('employee/update/<str:empid>/', views.employee_update_view, name='employee_update_view'),
    path('employee/update_search/', views.employee_update_search, name='employee_update_search'),
    path('suppliers/', views.supplier_list_view, name='supplier_list'),
    path('success/', views.success, name='success'),
    path('search/', views.search_hospitals_by_capital, name='hospital_search'),
    path('hospital_list', views.hospital_list, name='hospital_list'),
    path('edit_hospital/<str:tabyouinid>/', views.edit_hospital, name='edit_hospital'),

# 受付
    path('home2', views.home2, name='home2'),
    path('patient/register/', views.patient_register, name='patient_register'),
    path('patient/register/success/', views.patient_register_success, name='patient_register_success'),
    path('employee/password_change/', views.password_change_view, name='password_change'),
    path('employee/password_change_success/', views.password_change_success_view, name='password_change_success'),
    path('patient/search/', views.patient_search_view, name='patient_search'),
    path('patient/list/', views.patient_list, name='patient_list'),
    path('patient_insurance_edit/', views.patient_insurance_edit, name='patient_insurance_edit'),
    path('patient/edit/', views.patient_insurance_edit, name='patient_insurance_edit'),

# 医師
    path('doctor_home/', views.doctor_home, name='doctor_home'),
    path('patient_search/', views.patient_search_view2, name='patient_search_view2'),
    path('medication_order/<str:patid>/', views.medication_order_view, name='medication_order_view'),
    path('medication_confirm/<str:patid>/', views.medication_confirm_view, name='medication_confirm_view'),
    path('search_patient_by_id/', views.search_patient_by_id, name='search_patient_by_id'),
    path('search_patient_by_id2/', views.search_patient_by_id2, name='search_patient_by_id2'),

]