from django.urls import path
from . import views

urlpatterns=[
    path('',views.form_login,name="login"),
    path('signup/',views.form_signup,name='signup'),
    path('logout/',views.form_logout,name='logout'),
    path('create/',views.form_create,name='create'),
    path('display/',views.form_display,name="display"),
    path('delete/<int:pk>/',views.form_delete,name="delete"),
    path('edit/<int:pk>/',views.form_edit,name="edit"),
    path('view/<int:pk>/',views.form_view,name="view"),
    path('download/<int:pk>/',views.form_download,name="download"),
]