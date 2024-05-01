from django.urls import path
from .view import views, types_view, income_view, expense_view

urlpatterns = [
    path('', views.index, name='index'),
    path('expense/', expense_view.expense, name='expense'),
    path('expense/add/', expense_view.expense_add, name='expense_add'),
    path('expense/edit/', expense_view.expense_edit, name='expense_edit'),
    path('expense/delete/', expense_view.expense_delete, name='expense_delete'),
    path('income/', income_view.income, name='income'),
    path('income/add/', income_view.income_add, name='income_add'),
    path('income/edit/', income_view.income_edit, name='income_edit'),
    path('income/delete/', income_view.income_delete, name='income_delete'),
    path('type/', types_view.types, name='types'),
    path('type/edit/', types_view.types_edit, name='types_edit'),
    path('type/delete/', types_view.types_delete, name='types_delete')
]
