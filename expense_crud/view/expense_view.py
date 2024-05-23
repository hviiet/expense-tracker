from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.db.models import Q, Sum
from ..models import ExpenseType, Expense
from datetime import date, timedelta
import pandas as pd

def expense(request):
    user = request.user
    if request.method == 'GET':
        date_range_str = request.GET.get('date_range', '')
        if date_range_str != '':
            date_range = date_range_str.split(' - ')
            date_start = date_range[0].split('/')
            date_start = date(int(date_start[2]), int(date_start[1]), int(date_start[0]))
            date_end = date_range[1].split('/')
            date_end = date(int(date_end[2]), int(date_end[1]), int(date_end[0]))
        else:
            date_end = date.today()
            date_start = date_end - timedelta(days=7)
            date_range_str = date_start.strftime('%d/%m/%Y') + ' - ' + date_end.strftime('%d/%m/%Y')
        types_str = request.GET.get('types', '')
        if types_str == '':
            types = []
        else:
            types = list(map(int, types_str.split(',')))
        expense_types = ExpenseType.objects.filter(user=user)
        if len(types) > 0:
            expenses = Expense.objects.filter(
                user=user,
                expense_type__in=types,
                date__range=[date_start, date_end]
            ).order_by('-date')
        else:
            expenses = Expense.objects.filter(
                user=user,
                date__range=[date_start, date_end]
            ).order_by('-date')
        # Get data for pie chart
        expenses_group_by_type = Expense.objects.filter(
            user=request.user,
            date__range=[date_start, date_end]
        ).values('expense_type__name').annotate(total_amount=Sum('amount'))
        # Get data and labels
        expense_pie_labels = [expense['expense_type__name'] for expense in expenses_group_by_type]
        expense_pie_values = [expense['total_amount'] for expense in expenses_group_by_type]
        # Convert to string
        expense_pie_labels = '/'.join(expense_pie_labels) if expense_pie_labels else ''
        expense_pie_values = '/'.join([str(i) for i in expense_pie_values]) if expense_pie_values else ''

        return render(request, 'expense.html', {
            'user': user,
            'types': expense_types,
            'expenses': expenses,
            'total_amount': sum([expense.amount for expense in expenses]),
            'date_range_str': date_range_str,
            'types_search': types,
            'expense_pie_labels': expense_pie_labels,
            'expense_pie_values': expense_pie_values
        })
    
def expense_add(request):
    user = request.user
    if request.method == 'POST':
        amount = request.POST.get('amount')
        type_id = request.POST.get('type_id')
        date_str = request.POST.get('date')
        date_str = date_str.split('-')
        date_val = date(int(date_str[0]), int(date_str[1]), int(date_str[2]))
        description = request.POST.get('description')
        expense_type = ExpenseType.objects.filter(user=user, id=type_id).first()
        expense = Expense(user=user, amount=amount, expense_type=expense_type, date=date_val, description=description)
        expense.save()
        return JsonResponse({'status': 'success'})

def expense_add_excel(request):
    user = request.user
    if request.method == 'POST':
        excel_file = request.FILES['excel']
        df = pd.read_excel(excel_file)
        error_count = 0
        success_count = 0
        for index, row in df.iterrows():
            try:
                amount = float(str(row['Chi tiêu']).replace(',', '').replace('.', ''))
                type_name = row['Loại']
                date_str = row['Thời gian'].split('-')
                date_val = date(int(date_str[2]), int(date_str[1]), int(date_str[0]))
                description = row['Mô tả'] if type(row['Mô tả']) is str else ''
                expense_type = ExpenseType.objects.filter(user=user, name=type_name).first()
                if not expense_type:
                    expense_type = ExpenseType(user=user, name=type_name, description='')
                    expense_type.save()
                income = Expense(user=user, amount=amount, expense_type=expense_type, date=date_val, description=description)
                income.save()
                success_count += 1
            except:
                error_count += 1
                continue
        return JsonResponse({'status': 'success', 'error_count': error_count, 'success_count': success_count})

def expense_edit(request):
    user = request.user
    if request.method == 'GET':
        expense_id = request.GET.get('expense_id', None)
        expense = Expense.objects.filter(user=user, id=expense_id).first()
        if not expense:
            return JsonResponse(status=404)
        return JsonResponse({
            'expense_id': expense.id,
            'amount': expense.amount,
            'type_id': expense.expense_type.id,
            'date': expense.date,
            'description': expense.description
        })
    elif request.method == 'POST':
        expense_id = request.POST.get('expense_id')
        amount = request.POST.get('amount')
        type_id = request.POST.get('type_id')
        date_str = request.POST.get('date')
        date_str = date_str.split('-')
        date_val = date(int(date_str[0]), int(date_str[1]), int(date_str[2]))
        description = request.POST.get('description')
        expense = Expense.objects.filter(user=user, id=expense_id).first()
        expense.amount = amount
        expense.expense_type = ExpenseType.objects.filter(user=user, id=type_id).first()
        expense.date = date_val
        expense.description = description
        expense.save()
        return JsonResponse({'status': 'success'})
    
def expense_delete(request):
    user = request.user
    if request.method == 'GET':
        expense_id = request.GET.get('expense_id', None)
        expense = Expense.objects.filter(user=user, id=expense_id).first()
        if not expense:
            return JsonResponse(status=404)
        expense.delete()
        return JsonResponse({'status': 'success'})
    return HttpResponseBadRequest()