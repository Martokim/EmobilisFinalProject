from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('',views.home, name='home'),
    path('services/',views.services , name='services'),
    # path('contact/',views.contact , name='contact'), #working progres
    # path('projects/',views.projects, name='projects'), #working progress 
    path('plants/',views.plant_catalog,name='plant_catalog'),
    path('plants/<int:plant_id>/',views.plant_detail,name='plant_detail'),
    path('plants/<int:plant_id>/request/', views.request_plant, name='request_plant'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('my-plant-requests/', views.my_plant_requests, name='my_plant_requests'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('services/', views.services, name='services'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('request-quote/<int:service_id>/', views.request_quote, name='request_quote'),
    
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-plants/', views.manage_plants, name='manage_plants'),
    path('add-plant/', views.add_plant, name='add_plant'),
    path('edit-plant/<int:plant_id>/', views.edit_plant, name='edit_plant'),
    path('delete-plant/<int:plant_id>/', views.delete_plant, name='delete_plant'),

    path('manage-services/', views.manage_services, name='manage_services'),
    path('add-service/', views.add_service, name='add_service'),
    path('edit-service/<int:service_id>/', views.edit_service, name='edit_service'),
    path('delete-service/<int:service_id>/', views.delete_service, name='delete_service'),

    path('respond-to-request/<str:request_type>/<int:request_id>/', views.respond_to_request, name='respond_to_request'),

    path('add-to-cart/<int:plant_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
]



#For development purposes
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
