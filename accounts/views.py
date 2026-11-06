
from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm


def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = CustomerRegistrationForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })
