from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from .models import ExpenseType, IncomeType, User

def index(request):
    return render(request, 'index.html', {
        'user': request.user
    })

def expense_type(request):
    user = request.user
    if request.method == 'GET':
        i_page = request.GET.get('i_page', 1)
        e_page = request.GET.get('e_page', 1)

        income_types = IncomeType.objects.all()
        expense_types = ExpenseType.objects.all()
        return render(request, 'expense_type.html', {
            'user': user,
            'income_types': income_types,
            'expense_types': expense_types
        })
    elif request.method == 'POST':
        current_type = request.POST['current_type']
        name = request.POST['name']
        description = request.POST['description']
        if current_type == 'income':
            incomeType = IncomeType(name=name, description=description, user=user)
            incomeType.save()
            return JsonResponse({'message': 'Thêm thành công'})            
        elif current_type == 'expense':
            expenseType = ExpenseType(name=name, description=description, user=user)
            expenseType.save()
            return JsonResponse({'message': 'Thêm thành công'})

def expense_type_edit(request):
    if (request.method == 'GET'):
        current_id = request.GET.get('current_id', None)
        current_type = request.GET.get('current_type', None)
        if current_type == 'income':
            incomeType = IncomeType.objects.get(id=current_id)
            return JsonResponse({
                'name': incomeType.name,
                'description': incomeType.description
            })
        elif current_type == 'expense':
            expenseType = ExpenseType.objects.get(id=current_id)
            return JsonResponse({
                'name': expenseType.name,
                'description': expenseType.description
            })
        return HttpResponseBadRequest()
    elif (request.method == 'POST'):
        name = request.POST['name']
        current_id = request.POST['current_id']
        current_type = request.POST['current_type']
        description = request.POST['description']
        if current_type == 'income':
            incomeType = IncomeType.objects.get(id=current_id)
            incomeType.name = name
            incomeType.description = description
            incomeType.save()
            return JsonResponse({'message': 'Sửa thành công'})
        elif current_type == 'expense':
            expenseType = ExpenseType.objects.get(id=current_id)
            expenseType.name = name
            expenseType.description = description
            expenseType.save()
            return JsonResponse({'message': 'Sửa thành công'})
        return HttpResponseBadRequest()

def expense_type_delete(request):
    if (request.method == 'GET'):
        current_id = request.GET.get('current_id', None)
        current_type = request.GET.get('current_type', None)
        if current_type == 'income':
            incomeType = IncomeType.objects.get(id=current_id)
            incomeType.delete()
            return JsonResponse({'message': 'Xóa thành công'})
        elif current_type == 'expense':
            expenseType = ExpenseType.objects.get(id=current_id)
            expenseType.delete()
            return JsonResponse({'message': 'Xóa thành công'})
        return HttpResponseBadRequest()
