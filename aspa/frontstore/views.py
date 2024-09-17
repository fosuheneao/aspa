from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from aspamain.models import Category

from .forms import StoreForm

# @method_decorator(login_required, name='dispatch')
def load_categories(request):
    industry_id = request.GET.get('industry_id')
    categories = Category.objects.filter(industry_id=industry_id).order_by('name')
    return JsonResponse(list(categories.values('id', 'name')), safe=False)


@login_required
def create_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.save()
            return redirect('store_list')  # Redirect to a page listing stores or a confirmation page
    else:
        form = StoreForm(user=request.user)
    
    return render(request, 'frontstore/create_store.html', {'form': form})
# Create your views here.
@login_required
def dashboard(request):

    if request.user.is_authenticated:
        # assets = Asset.objects.filter(createdby_id = request.user.id)
        # assettypes = AssetType.objects.filter(createdby_id = request.user.id)
        # assets = Asset.objects.filter(createdby_id = request.user.id)
        return render(request, 'frontstore/dashboard.html')
    else:
        return redirect('login')


class LoginView(View):
    template_name = 'frontstore/login.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):

    # if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # A backend authenticated the credentials
            messages.success(request, f'welcome, {user.username}')
            return redirect('dashboard')
        else:
            # No backend authenticated the credentials
             messages.warning(request, 'Invalid login credentials!')
             return render(request, self.template_name)
         
         
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'Log out successful.')
        return redirect('login')
