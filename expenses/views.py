from django.shortcuts import render, redirect
from .models import Expense
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
@login_required
@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)

    # Calculate totals
    total = sum(exp.amount for exp in expenses)

    # Category totals
    categories = {}
    for exp in expenses:
        categories[exp.category] = categories.get(exp.category, 0) + exp.amount

    context = {
        'expenses': expenses,
        'total': total,
        'categories': categories
    }

    return render(request, 'dashboard.html', context)
# Create your views here.
@login_required
def add_expense(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        category = request.POST['category']
        date = request.POST['date']
        description = request.POST['description']

        Expense.objects.create(
            user=request.user,
            amount=amount,
            category=category,
            date=date,
            description=description
        )

        return redirect('dashboard')

    return render(request, 'add_expense.html')
@login_required
def export_csv(request):
    expenses = Expense.objects.filter(user=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Category', 'Date', 'Description'])

    for exp in expenses:
        writer.writerow([exp.amount, exp.category, exp.date, exp.description])

    return response