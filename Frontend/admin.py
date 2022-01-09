from django.contrib import admin

# Register your models here.

from Frontend.models import Product, AdminBanner, AdminBasicInfo, Order, Cart, BloodGroup, Blood, Ambulance, \
    AmbulanceOrder, DoctorSpecialist, Doctor, DoctorAppointment, CartProduct



@admin.register(AdminBanner)
class AdminBannerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'banner',
        'active',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'image',
        'price',
        'description',
        'material',
        'user',
        'date_created',
    )


@admin.register(AdminBasicInfo)
class AdminBasicInfoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'websiteName',
        'websiteTitle',
        'websiteSubTitle',
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'active',
    )


@admin.register(CartProduct)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'cart',
        'quantity',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'cart',
        'total_price',
    )


@admin.register(BloodGroup)
class BloodGroupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'group',
    )


@admin.register(Blood)
class BloodAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'blood',
        'address',
    )


@admin.register(Ambulance)
class AmbulanceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'user',
        'details',
        'contact_number',
        'cost',
        'image',
    )


@admin.register(AmbulanceOrder)
class AmbulanceOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ambulance',
        'user',
        'time',
    )


@admin.register(DoctorSpecialist)
class DoctorSpecialistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'image',
        "specialist"
    )


@admin.register(DoctorAppointment)
class DoctorAppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        "doctor",
        "time",
    )
