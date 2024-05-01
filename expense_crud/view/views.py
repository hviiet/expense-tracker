from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.db.models import Sum
from ..models import Expense, Income
from datetime import date, timedelta

def index(request):
    # Get date in range last 6 months
    current_date = date.today()
    start_day = current_date.replace(day=1).replace(month=current_date.month - 5 + (12 if current_date.month - 5 < 1 else 0)).replace(year=current_date.year - (1 if current_date.month - 5 < 1 else 0))
    end_day = current_date.replace(day=1).replace(month=(1 if current_date.month == 12 else current_date.month + 1)).replace(year=current_date.year + (1 if current_date.month == 12 else 0)) - timedelta(days=1)
    if (start_day.month >= 8):
        month_labels = [i for i in range(start_day.month, 13)] + [i for i in range(1, end_day.month + 1)]
    else:
        month_labels = [i for i in range(start_day.month, end_day.month + 1)]

    # Get data from database
    expenses = Expense.objects.filter(
            user=request.user,
            date__range=[start_day, end_day]
        ).order_by('-date').values('amount', 'date', 'expense_type')
    incomes = Income.objects.filter(
            user=request.user,
            date__range=[start_day, end_day]
        ).order_by('-date').values('amount', 'date', 'income_type')
    
    # Get data for bar chart
    expense_values = []
    income_values = []
    for month in month_labels:
        expense_filter = expenses.filter(date__month=month)
        if expense_filter:
            expense_values.append(sum([expense['amount'] for expense in expense_filter]))
        else:
            expense_values.append(0)
        income_filter = incomes.filter(date__month=month)
        if income_filter:
            income_values.append(sum([income['amount'] for income in income_filter]))
        else:
            income_values.append(0)
    total_expense = sum([value for value in expense_values])
    total_income = sum([value for value in income_values])
    expense_values = '/'.join([str(i) for i in expense_values])
    income_values = '/'.join([str(i) for i in income_values])
    month_labels = [f'Tháng {i}' for i in month_labels]
    month_labels = '/'.join(month_labels)

    # Get data for pie chart
    expenses_group_by_type = Expense.objects.filter(
        user=request.user,
        date__range=[start_day, end_day]
    ).values('expense_type__name').annotate(total_amount=Sum('amount'))
    incomes_group_by_type = Income.objects.filter(
        user=request.user,
        date__range=[start_day, end_day]
    ).values('income_type__name').annotate(total_amount=Sum('amount'))
    # Get data and labels
    expense_pie_labels = [expense['expense_type__name'] for expense in expenses_group_by_type]
    expense_pie_values = [expense['total_amount'] for expense in expenses_group_by_type]
    income_pie_labels = [income['income_type__name'] for income in incomes_group_by_type]
    income_pie_values = [income['total_amount'] for income in incomes_group_by_type]
    # Convert to string
    expense_pie_labels = '/'.join(expense_pie_labels) if expense_pie_labels else ''
    expense_pie_values = '/'.join([str(i) for i in expense_pie_values]) if expense_pie_values else ''
    income_pie_labels = '/'.join(income_pie_labels) if income_pie_labels else ''
    income_pie_values = '/'.join([str(i) for i in income_pie_values]) if income_pie_values else ''

    return render(request, 'statics.html', {
        'user': request.user,
        'expense_data': expense_values,
        'income_data': income_values,
        'month_labels': month_labels,
        'total_expense': total_expense,
        'total_income': total_income,
        'expense_pie_labels': expense_pie_labels,
        'expense_pie_values': expense_pie_values,
        'income_pie_labels': income_pie_labels,
        'income_pie_values': income_pie_values
    })