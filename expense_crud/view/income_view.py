from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.db.models import Q, Sum
from ..models import IncomeType, Income
from datetime import date, timedelta
import pandas as pd

def income(request):
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
        income_types = IncomeType.objects.filter(user=user)
        print(income_types)
        if len(types) > 0:
            incomes = Income.objects.filter(
                user=user,
                income_type__in=types,
                date__range=[date_start, date_end]
            ).order_by('-date')
        else:
            incomes = Income.objects.filter(
                user=user,
                date__range=[date_start, date_end]
            ).order_by('-date')

        # Get data for pie chart
        incomes_group_by_type = Income.objects.filter(
            user=request.user,
            date__range=[date_start, date_end]
        ).values('income_type__name').annotate(total_amount=Sum('amount'))
        # Get data and labels
        income_pie_labels = [income['income_type__name'] for income in incomes_group_by_type]
        income_pie_values = [income['total_amount'] for income in incomes_group_by_type]
        # Convert to string
        income_pie_labels = '/'.join(income_pie_labels) if income_pie_labels else ''
        income_pie_values = '/'.join([str(i) for i in income_pie_values]) if income_pie_values else ''

        return render(request, 'income.html', {
            'user': user,
            'types': income_types,
            'incomes': incomes,
            'total_amount': sum([income.amount for income in incomes]),
            'date_range_str': date_range_str,
            'types_search': types,
            'income_pie_labels': income_pie_labels,
            'income_pie_values': income_pie_values
        })
    
def income_add(request):
    user = request.user
    if request.method == 'POST':
        amount = request.POST.get('amount')
        type_id = request.POST.get('type_id')
        date_str = request.POST.get('date')
        date_str = date_str.split('-')
        date_val = date(int(date_str[0]), int(date_str[1]), int(date_str[2]))
        description = request.POST.get('description')
        income_type = IncomeType.objects.filter(user=user, id=type_id).first()
        income = Income(user=user, amount=amount, income_type=income_type, date=date_val, description=description)
        income.save()
        return JsonResponse({'status': 'success'})

def income_add_excel(request):
    user = request.user
    if request.method == 'POST':
        excel_file = request.FILES['excel']
        df = pd.read_excel(excel_file)
        error_count = 0
        success_count = 0
        for index, row in df.iterrows():
            try:
                amount = float(str(row['Thu nhập']).replace(',', '').replace('.', ''))
                type_name = row['Loại']
                date_str = row['Thời gian'].split('-')
                date_val = date(int(date_str[2]), int(date_str[1]), int(date_str[0]))
                description = row['Mô tả'] if type(row['Mô tả']) is str else ''
                income_type = IncomeType.objects.filter(user=user, name=type_name).first()
                if not income_type:
                    income_type = IncomeType(user=user, name=type_name, description='')
                    income_type.save()
                income = Income(user=user, amount=amount, income_type=income_type, date=date_val, description=description)
                income.save()
                success_count += 1
            except:
                error_count += 1
                continue
        return JsonResponse({'status': 'success', 'error_count': error_count, 'success_count': success_count})

def income_edit(request):
    user = request.user
    if request.method == 'GET':
        income_id = request.GET.get('income_id', None)
        income = Income.objects.filter(user=user, id=income_id).first()
        if not income:
            return JsonResponse(status=404)
        return JsonResponse({
            'income_id': income.id,
            'amount': income.amount,
            'type_id': income.income_type.id,
            'date': income.date,
            'description': income.description
        })
    elif request.method == 'POST':
        income_id = request.POST.get('income_id')
        amount = request.POST.get('amount')
        type_id = request.POST.get('type_id')
        date_str = request.POST.get('date')
        date_str = date_str.split('-')
        date_val = date(int(date_str[0]), int(date_str[1]), int(date_str[2]))
        description = request.POST.get('description')
        income = Income.objects.filter(user=user, id=income_id).first()
        income.amount = amount
        income.income_type = IncomeType.objects.filter(user=user, id=type_id).first()
        income.date = date_val
        income.description = description
        income.save()
        return JsonResponse({'status': 'success'})
    
def income_delete(request):
    user = request.user
    if request.method == 'GET':
        income_id = request.GET.get('income_id', None)
        income = Income.objects.filter(user=user, id=income_id).first()
        if not income:
            return JsonResponse(status=404)
        income.delete()
        return JsonResponse({'status': 'success'})
    return HttpResponseBadRequest()