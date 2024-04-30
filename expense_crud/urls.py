from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('type/', views.expense_type, name='expense_type'),
    path('type/edit/', views.expense_type_edit, name='expense_type_edit'),
    path('type/delete/', views.expense_type_delete, name='expense_type_delete')
]
