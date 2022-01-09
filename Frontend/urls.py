from django.contrib import admin
from django.urls import path
from . import views

app_name = 'front'
urlpatterns = [
    path('product/<int:pk>/', views.ProductPage.as_view(), name="product"),
    path('auth/login/', views.login_page, name="login"),
    path('auth/register/', views.RegisterPage.as_view(), name="register"),
    path('add/cart/<int:product_id>/', views.cart_a_product, name="cart_a_product"),
    path('all/cart/', views.AllCartProduct.as_view(), name="user_cart"),
    path('remove/cart_product/<int:pk>/', views.RemoveProductFromCart.as_view(), name="remove_cart_product"),
    path('cart/to/checkout/', views.cart_to_checkout, name="cart_to_checkout"),
    path('blood/', views.blood_page, name="blood"),
    path('product/all/', views.all_product, name="product_all"),
    path('ambulance/all/', views.ambulance_all, name="ambulance"),
    path('ambulance/order/<int:ambulance_id>/', views.order_ambulance, name="ambulance_order"),
    path('user/', views.user_page, name="user"),
    path('doctor/all/', views.DoctorList.as_view(), name="doctor"),
    path('doctor/appointment/<int:pk>/', views.appointment_doctor, name="doctor_appointment"),
    path('doctor/tele/', views.TeleDoctor.as_view(), name="tele_doctor"),
    path('doctor/video/tele/', views.VideoDoctor.as_view(), name="tele_doctor_video"),
    path('doctor/remove/appointment/<int:pk>/', views.RemoveDoctorAppointment.as_view(), name="remove_doctor_appointment"),
    path('logout/', views.logout_user, name="logout"),
    path('', views.Index.as_view(), name='index'),

    #     api call
    path('api/check/cart/count/', views.cart_count)
]
