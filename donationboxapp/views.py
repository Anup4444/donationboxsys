from django.shortcuts import render, redirect
from .forms import ContactForm

# Create your views here.


def Index(request):
    return render(request, 'donationboxapp/index.html')


def About(request):
    return render(request, 'donationboxapp/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')  # Redirect to a success page
    else:
        form = ContactForm()

    return render(request, 'donationboxapp/contact.html', {'form': form})


def Programs(request):
    return render(request, 'donationboxapp/services.html')
