from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Plant, CartItem ,PlantRequest, Service, QuoteRequest, UserProfile, Order ,OrderItem
from .forms import UserRegisterForm, UserProfileForm, PlantRequestForm, QuoteRequestForm
from django.db import models
from django.utils.html import strip_tags
from .forms import ServiceForm, PlantForm




def get_or_create_user_profile(user):
    try:
        return user.userprofile
    except UserProfile.DoesNotExist:
        return UserProfile.objects.create(user=user)


# Create your views here.
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form}) 

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    total_spent = Order.objects.filter(user=request.user).aggregate(total=models.Sum('total_amount'))['total'] or 0

    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserRegisterForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'plant_requests': PlantRequest.objects.filter(user=request.user).order_by('-request_date'),
        'quote_requests': QuoteRequest.objects.filter(user=request.user).order_by('-created_at'),
        'total_spent': total_spent,
    }
    return render(request, 'profile.html', context)



def services(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})


def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'service_detail.html', {'service': service})


# request quote view
@login_required
def request_quote(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    user_profile = get_or_create_user_profile(request.user)
    if request.method == 'POST':
        form = QuoteRequestForm(request.POST, request.FILES)
        if form.is_valid():
            quote_request = form.save(commit=False)
            quote_request.user = request.user
            quote_request.service = service
            quote_request.save()
            messages.success(request, 'Your quote request has been submitted successfully!')
            return redirect('profile')
    else:
        form = QuoteRequestForm(initial={
            'service': service,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone': request.user.userprofile.phone_number
        })
    return render(request, 'request_quote.html', {'form': form, 'service': service})

# Admin dashboard view
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    plant_requests = PlantRequest.objects.filter(status='pending').order_by('request_date')
    quote_requests = QuoteRequest.objects.filter(status='pending').order_by('created_at')
    return render(request, 'admin_dashboard.html', {'plant_requests': plant_requests, 'quote_requests': quote_requests})

# view for responding to requests
@user_passes_test(lambda u: u.is_staff)
def respond_to_request(request, request_type, request_id):
    if request_type == 'plant':
        req = get_object_or_404(PlantRequest, id=request_id)
    elif request_type == 'quote':
        req = get_object_or_404(QuoteRequest, id=request_id)
    else:
        messages.error(request, 'Invalid request type')
        return redirect('admin_dashboard')

    if request.method == 'POST':
        status = request.POST.get('status')
        response = request.POST.get('response')

         # Validate the status input
        VALID_STATUSES = ['Pending', 'Inprogress' ,'Completed']
        if status not in VALID_STATUSES:
            messages.error(request, 'Invalid status selected.')
            return redirect('respond_to_request', request_type=request_type, request_id=request_id)

        req.status = status
        req.save()
        # Send email to user
        subject = f"Update on your {request_type} request"
        html_message = render_to_string('email/request_update.html', {
            'user': req.user,
            'request_type': request_type,
            'status': status,
            'response': response,
        })
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = req.user.email
        
        if not to_email:
            messages.error(request,f"User{req.user.username} has no email configured.")
        else:
            try:
                send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
                messages.success(request, f'{request_type.capitalize()} request has been updated and user notified.')
            except Exception as e:
                messages.error(request, f"Error sending email: {e}")

        return redirect('admin_dashboard')

    #request details and type to the template
    # Handle GET request to render the response form
    context = {
        'req': req,
        'request_type': request_type,
    }
    return render(request, 'respond_to_request.html', context)

     
#view for requesting a plant 
@login_required
def request_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    user_profile = get_or_create_user_profile(request.user)
    if request.method == 'POST':
        form = PlantRequestForm(request.POST)
        if form.is_valid():
            plant_request = form.save(commit=False)
            plant_request.user = request.user
            plant_request.plant = plant
            plant_request.save()
            messages.success(request, f'Your request for {plant.name} has been submitted!')
            return redirect('plant_detail', plant_id=plant.id)
    else:
        form = PlantRequestForm(initial={
            'delivery_address': request.user.userprofile.address,
            'phone_number': request.user.userprofile.phone_number
        })
    return render(request, 'request_plant.html', {'form': form, 'plant': plant})

# Plant view catalogue
def plant_catalog(request):
    plants = Plant.objects.all()
    return render(request, 'plant_catalog.html', {'plants': plants})

# plant detail view
def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    return render(request, 'plant_detail.html', {'plant': plant})

# view for lissting user plant requests
@login_required
def request_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == 'POST':
        form = PlantRequestForm(request.POST)
        if form.is_valid():
            plant_request = form.save(commit=False)
            plant_request.user = request.user
            plant_request.plant = plant
            plant_request.save()
            messages.success(request, f"Your request for {plant.name} has been submitted successfully!")
            return redirect('plant_detail', plant_id=plant.id)
    else:
        form = PlantRequestForm()
    return render(request, 'request_plant.html', {'form': form, 'plant': plant})

@login_required
def my_plant_requests(request):
    plant_requests = PlantRequest.objects.filter(user=request.user).order_by('-request_date')
    return render(request, 'my_plant_requests.html', {'plant_requests': plant_requests})

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    
    if request.method == 'POST':
        # Collect delivery details
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            address=address,
            phone=phone,
            email=email
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                plant=item.plant,
                quantity=item.quantity,
                price=item.plant.price
            )
        cart_items.delete()

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_confirmation', order_id=order.id)
    
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmation.html', {'order': order})

@login_required
def add_to_cart(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, plant=plant)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{plant.name} added to your cart.")
    return redirect('plant_detail', plant_id=plant.id)

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    plant_name = cart_item.plant.name
    cart_item.delete()
    messages.success(request, f"{plant_name} removed from your cart.")
    return redirect('view_cart')
    
@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f"Quantity updated for {cart_item.plant.name}.")
    else:
        plant_name = cart_item.plant.name
        cart_item.delete()
        messages.success(request, f"{plant_name} removed from your cart.")
    return redirect('view_cart')

#CRUD FUNCTIONALITY INCLUDED IN ADMIN-DASHBOARD
@user_passes_test(lambda u: u.is_staff)
def manage_plants(request):
    plants = Plant.objects.all()
    return render(request, 'manage_plants.html', {'plants': plants})

@user_passes_test(lambda u: u.is_staff)
def manage_services(request):
    services = Service.objects.all()
    return render(request, 'manage_services.html', {'services': services})

@user_passes_test(lambda u: u.is_staff)
def add_plant(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plant added successfully!')
            return redirect('manage_plants')
    else:
        form = PlantForm()
    return render(request, 'add_edit_plant.html', {'form': form, 'action': 'Add'})

@user_passes_test(lambda u: u.is_staff)
def edit_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plant updated successfully!')
            return redirect('manage_plants')
    else:
        form = PlantForm(instance=plant)
    return render(request, 'add_edit_plant.html', {'form': form, 'action': 'Edit'})

@user_passes_test(lambda u: u.is_staff)
def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    plant.delete()
    messages.success(request, 'Plant deleted successfully!')
    return redirect('manage_plants')

@user_passes_test(lambda u: u.is_staff)
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added successfully!')
            return redirect('manage_services')
    else:
        form = ServiceForm()
    return render(request, 'add_edit_service.html', {'form': form, 'action': 'Add'})

@user_passes_test(lambda u: u.is_staff)
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully!')
            return redirect('manage_services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'add_edit_service.html', {'form': form, 'action': 'Edit'})

@user_passes_test(lambda u: u.is_staff)
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    messages.success(request, 'Service deleted successfully!')
    return redirect('manage_services')
