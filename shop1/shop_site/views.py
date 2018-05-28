import hashlib
import datetime

from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Merch, Cart, UserTokenStorage
from .forms import CheckoutForm
# Create your views here.

# Helpers
def getCart(user):
    """Function to cut on redundancy

    Attempts to get cart belonging to user, and creates one if there is none.
    """
    try:
        cart = Cart.objects.get(owner=user)
    except Cart.DoesNotExist:
        cart = Cart(owner=user)
        cart.save()
    return cart

def generateToken(username, password, date, user):
    token = hashlib.sha256()
    token.update(bytes(''.join([str(date), username, password]), 'utf8'))
    stored_token = UserTokenStorage(token=token.hexdigest(), expires=date+datetime.timedelta(hours=1), user=user)
    stored_token.save()
    print('Generated token for user:', user.username)
    return token.hexdigest()

def checkTokenFreshness(user_token):
    if timezone.now() > user_token.expires:
        print("Token for user", user_token.user.username, "expired")
        user_token.delete()
        return False
    else:
        print("Token for user", user_token.user.username, "is still good")
        return True

# Views
def index(request):
    """View function for index page.

    Sends list of all merch in shop.
    """
    merch_list = Merch.objects.order_by('name')
    context = {'merch_list': merch_list}
    return render(request, 'shop_site/index.html', context)

def login(request):
    """View function for login page.

    Uses Django-provided login form. Really fricking short.
    """
    return render(request, 'shop1/registration/login.html')

def logout(request):
    """View function for logout page.

    Even shorter.
    """
    return HttpResponse("Bye!")

def cart(request):
    """View function for cart page.

    Checks if user is logged in, adds or removes merch from cart, and sends
    it's contents to page.
    """
    if request.user.is_authenticated:
        cart = getCart(request.user)
        if request.method == "POST":
            if 'buy' in request.POST:
                merch = get_object_or_404(Merch, pk=request.POST['merchid'])
                merchnum = request.POST['merchnum']
                cart.add_merch(merch, merchnum)
                cart.save()
                merch.quantity = merch.quantity - int(merchnum)
                merch.save()
                return HttpResponseRedirect(reverse('cart'))
            elif 'remove' in request.POST:
                merch = get_object_or_404(Merch, pk=request.POST['merchid'])
                merchnum = request.POST['merchnum']
                cart.sub_merch(merch, merchnum)
                cart.save()
                merch.quantity = merch.quantity + int(merchnum)
                merch.save()
                return HttpResponseRedirect(reverse('cart'))
        context = {'cart': cart.contents(), 'cost': cart.total_summ()}
        return render(request, 'shop_site/cart.html', context)
    else:
        return render(request, 'shop_site/noway.html')
    return HttpResponse("How did you even get here.")

def detail(request, merch_id):
    """View function for detail page.

    Spits 404 at user if no such merch found.
    """
    merch = get_object_or_404(Merch, pk=merch_id)
    return render(request, 'shop_site/detail.html', {'merch': merch})

def checkout(request):
    """View function for checkout page.

    Checks if user is logged in, and sends him in appropriate place.
    """
    if request.user.is_authenticated:
        context = {'form': CheckoutForm()}
        return render(request, 'shop_site/checkout.html', context)
    else:
        return render(request, 'shop_site/noway.html')
    return HttpResponse("How did you even get here.")

def purchase(request):
    """View function for purchase page.

    Clears cart and says everything is okay.
    """
    if request.user.is_authenticated:
        cart = getCart(request.user)
        cart.delete()
        context = {'result': True}
        return render(request, 'shop_site/purchase.html', context)
    else:
        return render(request, 'shop_site/noway.html')
    return HttpResponse("How did you even get here.")

def cl_index(request):
    merch_list = Merch.objects.order_by('name')
    content = []
    for item in merch_list:
        content.append({"name": item.name, "price": item.price, "quantity": item.quantity, "desc": item.desc, "image": item.image, "id": item.id})
    return JsonResponse(content, safe=False)

@csrf_exempt
def cl_login(request):
    user = authenticate(username = request.POST['user'], password = request.POST['password'])
    if user:
        date = timezone.now()
        try:
            user_token = UserTokenStorage.objects.get(user=user)
        except UserTokenStorage.DoesNotExist:
            token_to_send = generateToken(request.POST['user'], request.POST['password'], date, user)
        else:
            print("Found token for user", user.username)
            if checkTokenFreshness(user_token):
                token_to_send = user_token.token
            else:
                token_to_send = generateToken(request.POST['user'], request.POST['password'], date, user)
        return HttpResponse(token_to_send, content_type='text/plain')
    else:
        response = HttpResponse()
        response.status_code = 401
        response.write('Login attempt failed. Try again.')
        return response
    return HttpResponse("This cannot continue.")

def cl_chk(token):
    try:
        user_token = UserTokenStorage.objects.get(token=token)
    except UserTokenStorage.DoesNotExist:
        print("Token does not exist or malformed.")
        return None
    if checkTokenFreshness(user_token):
        return user_token
    else:
        return None

@csrf_exempt
def cl_cart(request):
    token = cl_chk(request.POST['token'])
    if token:
        cart = getCart(token.user)
        if request.POST['submethod'] == 'get':
            content = []
            for item in cart.contents():
                content.append({"id": item[0].id, "num": item[1]})
            return JsonResponse(content, safe=False)
        elif request.POST['submethod'] == 'change':
            merch = get_object_or_404(Merch, pk=request.POST['merchid'])
            merchnum = request.POST['merchnum']
            content = None
            if int(merchnum) > 0:
                cart.add_merch(merch, merchnum)
                cart.save()
                merch.quantity = merch.quantity - int(merchnum)
                merch.save()
                content = {"merch+": merch.id, "quantity": merch.quantity}
            elif int(merchnum) < 0:
                cart.sub_merch(merch, merchnum)
                cart.save()
                merch.quantity = merch.quantity + abs(int(merchnum))
                merch.save()
                content = {"merch-": merch.id, "quantity": abs(int(merchnum))}
            return JsonResponse(content, safe=False)
        else:
            response = HttpResponse()
            response.status_code = 400
            response.write('Bad request received.')
            return response
    else:
        response = HttpResponse()
        response.status_code = 401
        response.write('Unauthorized access.')
        return response

@csrf_exempt
def cl_reg(request):
    response = HttpResponse()
    try:
        test = User.objects.get(username=request.POST['user'])
    except User.DoesNotExist:
        user = User.objects.create_user(request.POST['user'], '', request.POST['password'])
        if user:
            response.status_code = 200
            return response
        else:
            response.status_code = 401
            response.write('Credentials are invalid.')
            return response
    if test:
        response.status_code = 401
        response.write('Username is already taken.')
        return response

@csrf_exempt
def cl_check(request):
    token = cl_chk(request.POST['token'])
    if token:
        cart = getCart(token.user)
        cart.delete()
        return HttpResponse("OK")
    else:
        response = HttpResponse()
        response.status_code = 401
        response.write('Unauthorized access.')
        return response


class Reg(generic.CreateView):
    """View function for registration page.

    Uses Django-provided registration form.
    """
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'shop_site/register.html'
