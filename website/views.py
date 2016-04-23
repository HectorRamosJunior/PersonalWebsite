from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, 'website/index.html')

def redirect_view(request):
    return redirect('/')
