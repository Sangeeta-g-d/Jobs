from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name="index"),
    path('admin_db',views.admin_db,name='admin_db'),
    path('v3_login',views.v3_login,name='v3_login'),
    path('register',views.register,name='register'),
    path('admin_logout',views.admin_logout,name="admin_logout"),
    path('job_details',views.job_details,name="job_details"),
    path('add_job',views.add_job,name="add_job"),
    path('get_job_details/<int:id>/', views.get_job_details, name='get_job_details'),
    path('edit_job_details/<int:id>/', views.edit_job_details, name='edit_job_details'),
    path('delete_job/<int:id>/', views.delete_job, name='delete_job'),
    path('login',views.user_login,name='user_login'),
    path('user_registration',views.user_registration,name='user_registration'),
    path('jobs',views.jobs,name='jobs'),
    path('dashboard',views.user_dashboard,name='user_dashboard'),
    path('company_register',views.company_register,name='company_register'),
    path('company_login',views.company_login,name='company_login'),
    path('company_list',views.company_list,name='company_list'),
    path('toggle-approval/<int:user_id>/', views.toggle_approval, name='toggle_approval'),
    path('company_db',views.company_db,name='company_db'),
    path('company_add_job',views.company_add_job,name='company_add_job'),
    path('company_base',views.company_base,name='company_base'),
    path("get-user-details/", views.get_user_details, name="get-user-details"),
    path("apply-job/",views.apply_job,name="apply-job"),
    path('company_job_details',views.company_job_details,name="company_job_details"),
    path('company_edit_job_details/<int:id>/', views.company_edit_job_details, name='company_edit_job_details'),
    path('company_applied_jobs',views.company_applied_jobs,name="company_applied_jobs"),
    path('c_applied_candidates/<int:job_id>/', views.c_applied_candidates, name='c_applied_candidates'),
    path('toggle_job_status/<int:job_id>/', views.toggle_job_status, name='toggle_job_status'),
    path('a_company_jobs/<int:id>/', views.a_company_jobs, name='a_company_jobs'),
    path('a_candidate_details/<int:id>/', views.a_candidate_details, name='a_candidate_details'),
    path('user_profile/',views.user_profile,name="user_profile"),


    # Password reset paths
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]