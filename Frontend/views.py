import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Sum, F
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, DeleteView, CreateView, FormView

# Create your views here.
from django.views.generic.detail import SingleObjectMixin

from Frontend.forms import UserLoginForm, UserRegisterForm, BloodForm, ProductForm, AmbulanceForm
from Frontend.models import AdminBanner, Product, Cart, CartProduct, AdminBasicInfo, Order, Blood, BloodGroup, \
    Ambulance, AmbulanceOrder, Doctor, DoctorAppointment


class Index(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["banner"] = AdminBanner.objects.filter(active=True).first()
        context["products"] = Product.objects.all()[:6]
        context["basic"] = AdminBasicInfo.objects.first()
        context["new_products"] = Product.objects.filter(
            date_created__date=datetime.date.today() - datetime.timedelta(days=1))
        return context


class ProductPage(DetailView):
    template_name = "product.html"
    model = Product


def cart_a_product(request, product_id):
    if request.method == 'POST':
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=request.user, active=True)
            cartProd = CartProduct.objects.filter(cart=cart[0], product_id=product_id).first()
            if cartProd:
                cartProd.quantity = request.POST.get('quantity')
                cartProd.save()
            else:
                CartProduct(cart=cart[0], product_id=product_id, quantity=request.POST.get('quantity')).save()
            messages.success(request, 'Cart successfully.')
        else:
            messages.error(request, 'Login first.')
            return redirect("front:login")

        return redirect(request.META.get('HTTP_REFERER'))


class RemoveProductFromCart(DeleteView):
    model = CartProduct

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


@method_decorator(login_required, name='dispatch')
class RemoveDoctorAppointment(DeleteView):
    model = DoctorAppointment

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class AllCartProduct(ListView):
    template_name = "cart.html"
    # model = Cart
    context_object_name = 'cart'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_price'] = CartProduct.objects.select_related("product").filter(
            cart__user_id=self.request.user).aggregate(total_price=Sum(F('quantity') * F('product__price')))
        return context

    def get_queryset(self, **kwargs):
        return Cart.objects.prefetch_related("get_cart_products__product").filter(user=self.request.user,
                                                                                  active=True).first()


@login_required(login_url='/auth/login')
def cart_to_checkout(request):
    if request.method == "POST":
        total_price = CartProduct.objects.select_related("product").filter(
            cart__user_id=request.user).aggregate(total_price=Sum(F('quantity') * F('product__price')))
        print("total price : ", total_price['total_price'])
        cart = Cart.objects.get(user=request.user, active=True)
        Order(cart=cart, total_price=total_price['total_price']).save()
        cart.active = False
        cart.save()
        messages.success(request, "Successfully added to order.")
        return redirect("front:index")


def login_page(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            nextID = request.GET.get('next', None)
            if nextID is not None:
                return HttpResponseRedirect(request.GET.get('next'))
            else:
                return redirect('front:index')
        else:
            messages.info(request, 'invalid registration details')
    else:
        form = UserLoginForm()
    return render(request,'login.html',{'form':form})



class RegisterPage(FormView):
    template_name = 'register.html'
    model = User
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "User saved.")
        return super().form_valid(form)


def blood_page(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = BloodForm(request.POST)
            if form.is_valid():
                blood_id = form.cleaned_data['blood']
                address = form.cleaned_data['address']
                blood = BloodGroup.objects.get(group=blood_id)
                print(blood)
                Blood(user=request.user, blood=blood, address=address).save()
                messages.success(request, 'Blood added to group.')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(request, 'You should login first.')
            return redirect("/auth/login?next=/blood/")

    else:
        form = BloodForm()
    bloods = Blood.objects.select_related("user", "blood").all()
    return render(request, 'blood.html', {'form': form, 'bloods': bloods})


def all_product(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = request.user
                data.save()
                messages.success(request, 'Product created successfully.')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "Please login first.")
            return redirect('/auth/login?next=/product/all/')

    else:
        form = ProductForm()

    products = Product.objects.all()
    if request.user.is_authenticated:
        seller_products = Product.objects.filter(user=request.user).all()
    else:
        seller_products = Product.objects.none()
    return render(request, 'allProduct.html',
                  {'form': form, "seller_products": seller_products, 'products': products})


def ambulance_all(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = AmbulanceForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = request.user
                data.save()
                messages.success(request, 'Ambulance created successfully.')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "Please login first.")
            return redirect('/auth/login?next=/product/all/')

    else:
        form = AmbulanceForm()
    if request.user.is_authenticated:
        my_ambulances = Ambulance.objects.filter(user=request.user).all()
        ambulance_cart = AmbulanceOrder.objects.select_related("ambulance", "user").filter(user=request.user).all()
    else:
        my_ambulances = Ambulance.objects.none()
        ambulance_cart = AmbulanceOrder.objects.none()

    ambulances = Ambulance.objects.all()
    return render(request, 'ambulance.html',
                  {'form': form, 'my_ambulances': my_ambulances, 'ambulances': ambulances, 'orders': ambulance_cart})


def order_ambulance(request, ambulance_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            ambulaceInt = Ambulance.objects.get(pk=ambulance_id)
            AmbulanceOrder(ambulance=ambulaceInt, user=request.user, time=request.POST.get('time')).save()
            messages.success(request, 'Ambulance order successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect("/auth/login?next=/ambulance/all/")
    return redirect("front:index")


@login_required(login_url='/auth/login')
def user_page(request):
    carts = Cart.objects.prefetch_related("get_cart_products__product").filter(user=request.user, active=False)
    ambulances = AmbulanceOrder.objects.filter(user=request.user).all()
    appointments = DoctorAppointment.objects.filter(user=request.user).all()
    return render(request, 'user.html', {'carts': carts, 'ambulances': ambulances, 'appointments': appointments})


class DoctorList(TemplateView):
    template_name = "doctors.html"

    def get_context_data(self, **kwargs):
        context = super(DoctorList, self).get_context_data()
        context['doctors'] = Doctor.objects.all()
        if self.request.user.is_authenticated:
            context['appointments'] = DoctorAppointment.objects.select_related('doctor', 'user').filter(
                user=self.request.user)
        else:
            context['appointments'] = DoctorAppointment.objects.none()
        return context


def appointment_doctor(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            doctor = Doctor.objects.get(pk=pk)
            if doctor:
                DoctorAppointment(doctor=doctor, user=request.user, time=request.POST['time']).save()
                return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect("/auth/login/?next=/doctor/all/")


class TeleDoctor(ListView):
    template_name = 'tele_doctor.html'
    model = Doctor
    context_object_name = 'doctors'


class VideoDoctor(ListView):
    template_name = "tele_doctor.html"
    model = Doctor
    context_object_name = 'doctors'
    # camera = cv2.VideoCapture(0)
    # while True:
    #     return_value, image = camera.read()
    #     cv2.imshow('image', image)
    #     if cv2.waitKey(1) & 0xFF == ord('s'):
    #         cv2.imwrite('./media/test.jpg', image)
    #         break
    # camera.release()
    # cv2.destroyAllWindows()
    # return render(request, 'tele_doctor.html')


def cart_count(request):
    if request.is_ajax():
        info = AdminBasicInfo.objects.first()
        if request.user.is_authenticated:
            cart = Cart.objects.prefetch_related("get_cart_products").filter(user=request.user, active=True).first()
            if cart:
                return JsonResponse({'data': cart.get_cart_products.count(), 'infos': info.websiteName})
            else:
                return JsonResponse({'data': 0, 'infos': info.websiteName})
        else:
            return JsonResponse({"data": 0, 'infos': info.websiteName})
            # return JsonResponse({'data': 0, 'infos': info.websiteName},safe=False)
