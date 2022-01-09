from django.contrib import admin

# Register your models here.
from Frontend.forms import UserAdminChangeForm, UserAdminCreationForm
from Frontend.models import Product, AdminBanner, AdminBasicInfo, Order, Cart, Users, BloodGroup, Blood, Ambulance, \
    AmbulanceOrder, DoctorSpecialist, Doctor, DoctorAppointment, CartProduct
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['id', 'phone_number', 'admin', 'staff']
    list_filter = ['admin','staff']
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ("name",)}),
        ('Permissions', {'fields': ('admin','staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'phone_number', 'password1', 'password2', 'admin', 'staff')}
         ),
    )
    search_fields = ['phone_number']
    ordering = ['phone_number']
    filter_horizontal = ()


admin.site.register(Users, UserAdmin)


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
