from django.urls import path
from . import views

urlpatterns = [

    path('admin_db',views.admin_db,name='admin_db'),
    path('v3_login',views.v3_login,name='v3_login'),
    path('register',views.register,name='register'),
    path('admin_logout',views.admin_logout,name="admin_logout"),
    path('job_details',views.job_details,name="job_details"),
    path('add_job',views.add_job,name="add_job"),
    path('get_job_details/<int:id>/', views.get_job_details, name='get_job_details'),
]