from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, name, phone_number, password, **extra_fields):
        if Users.objects.filter(phone_number=phone_number).count() > 0:
            raise ValidationError(_('Phone number is already taken'))
        if not phone_number:
            raise ValidationError(_('Phone number is required'))
        if len(phone_number) != 11:
            raise ValidationError(_('Phone number must be 11 number'))
        if phone_number[0] != '0' and phone_number[1] != '1':
            raise ValidationError(_('Phone number must be start with 01'))
        if not password:
            raise ValidationError(_('Password is required'))
        if not phone_number.isnumeric():
            raise ValidationError(_('Phone number must be numeric'))
        extra_fields.setdefault("active", True)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.last_login = timezone.now()
        user.name = name.title()
        user.save(using=self._db)
        return user

    def create_staff(self, name, phone_number, password, **extra_fields):
        extra_fields.setdefault('staff', True)
        extra_fields.setdefault('active', True)
        if extra_fields.get('staff') is not True:
            raise ValueError(_('Seller must be true'))
        return self.create_user(name, phone_number, password, **extra_fields)

    def create_superuser(self, name, phone_number, password, **extra_fields):
        extra_fields.setdefault("staff", True)
        extra_fields.setdefault("admin", True)
        extra_fields.setdefault("active", True)
        user = self.create_user(name, phone_number, password, **extra_fields)
        return user


class Users(AbstractBaseUser):
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    name = models.CharField(_('Your name'), max_length=100,
                            validators=[
                                RegexValidator(
                                    regex=r'^[a-zA-Z ]*$',
                                    message=_('name must be Alpha'),
                                ),
                            ]
                            )
    phone_number = models.CharField(_('Phone number'), max_length=11, unique=True)
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['name']
    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_seller(self):
        return self.seller

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin


# Create your models here.
class AdminBanner(models.Model):
    banner = models.ImageField()
    active = models.BooleanField(default=True)


class AdminBasicInfo(models.Model):
    websiteName = models.CharField(max_length=255, verbose_name="Website name")
    websiteTitle = models.CharField(max_length=255, verbose_name="Website tile")
    websiteSubTitle = models.CharField(max_length=255, verbose_name="Website subtitle")


class Product(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    description = models.TextField()
    material = models.TextField(verbose_name="Product material")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_product")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_cart")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.name


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="get_product")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="get_cart_products")
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.product.name

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="get_cart_order")
    total_price = models.PositiveIntegerField()


class BloodGroup(models.Model):
    BLOOD_GROUP_OPTIONS = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )
    group = models.CharField(max_length=3, choices=BLOOD_GROUP_OPTIONS, unique=True)

    def __str__(self):
        return self.group


class Blood(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_blood")
    blood = models.ForeignKey(BloodGroup, on_delete=models.CASCADE, related_name="user_blood_group")
    address = models.TextField()

    def __str__(self):
        return self.user.name + "-" + self.blood.group


class Ambulance(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_ambulance")
    name = models.CharField(max_length=255)
    details = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=11)
    image = models.ImageField()
    cost = models.PositiveIntegerField()

    def __str__(self):
        return self.user.name + " " + self.contact_number


class AmbulanceOrder(models.Model):
    ambulance = models.ForeignKey(Ambulance, on_delete=models.CASCADE, related_name="ambulance_detail")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_ambulance_order")
    time = models.DateTimeField()

    def __str__(self):
        return self.user.name + " - " + self.ambulance.name + " - " + str(self.time.date())


class DoctorSpecialist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField()
    specialist = models.ForeignKey(DoctorSpecialist, on_delete=models.CASCADE, related_name="get_specialist_doctor")

    def __str__(self):
        return self.name


class DoctorAppointment(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="get_doctor_schedule")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="get_doctor")
    time = models.DateTimeField()
