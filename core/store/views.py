# from django.shortcuts import render,HttpResponse
# from django.template import loader
from .models import Book,Order,CartItem
# from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django import forms
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
# from .forms import CustomUserCreationForm
from django.contrib import messages

# from django.contrib.auth import authenticate, login, logout  # Import authentication functions
from django.contrib.auth.decorators import login_required  # Import login_required decorator
# from django.shortcuts import render, redirect
# from django.contrib import messages  # Import messages framework for user feedback


from .models import Book

def home(request):
    books = Book.objects.all()
    return render(request, "home.html", {"books": books})

def register_view(request):

    if request.method == 'POST':
        first_name= request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username= request.POST.get ('username')
        # first_name=request.POST.get("username")
        password= request.POST.get('password')
        print('fist name and pass',first_name,password)

        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'This usrname already taken')
            return redirect('/register/')


        user=User.objects.create(
        first_name=first_name,
        last_name=last_name,
        username=username,
        password=password,
        )
        user.save()
        # user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, 'Account created and logged in successfully')
        # messages.info(request,"account created successesfully")
    return render(request, 'signup.html', { })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.info(request, 'Invalid username')
            return render(request, 'Login.html', {})
        
        # Custom logic to compare plain text password with stored password (not recommended)
        if user.password == password:  # This is risky - don't do this
            login(request, user)
            messages.info(request, 'Login Successfully')
            return redirect('home')
        else:
            messages.info(request, 'Invalid password')
            return render(request, 'Login.html', {})
    return render(request, 'Login.html', {})
    



def logout_view(request):
    logout(request)
    return render(request, 'Logout.html',{})



@login_required(login_url='/login/')  # Require login for cart view
def cart_view(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user).select_related('book')  # Optimize query
  
    total = 0
    for item in cart_items.all():
        total += item.get_total_price()
    # return total





    context = {'cart_items': cart_items,'cart_total':total}
    # context = {'cart_items': cart_items,'cart_total':500}

    return render(request, 'cart.html', context)


@login_required(login_url='/login/')  # Require login for add_to_cart
def add_to_cart(request, book_id):
    user = request.user

    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        messages.info(request, 'Book not found')
        return redirect('home')

    
    existing_item = CartItem.objects.filter(user=user, book=book).first()
    # print("status: ",existing_item.status)
    if existing_item:
        if existing_item.status==False:
            existing_item.quantity += 1
            existing_item.save()
            # messages.info(request, f'Quantity of "{book.title}" in cart updated to {user.username}')
        else:
            new_cart_item = CartItem.objects.create(user=user, book=book)
    else:
        new_cart_item = CartItem.objects.create(user=user, book=book)
        # messages.info(request, f'"{book.title}" added to your cart')
        print("cart should be created")

    return redirect('home')  




@login_required(login_url='/login/')  
def remove_from_cart(request, book_id):
    user = request.user

    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        messages.info(request, 'Book not found')
        return redirect('home')

    existing_item = CartItem.objects.filter(user=user, book=book).first()

    if existing_item:
        existing_item.delete()
        # messages.info(request, f'"{book.title}" removed from your cart')
        print(request, f'"{book.title}" removed from your cart')

    else:
        # messages.info(request, f'"{book.title}" not in your cart')
        print(request, f'"{book.title}" not in your cart')


    return redirect('cart')  



@login_required(login_url='/login/')  
def checkout(request):
    user = request.user
    item=CartItem.objects.filter(user=user)
    if item:
        print("item exist: ",item)
    else:
        print("item is not present",item)
   
    try:
        order=Order.objects.create(user=user )
        order.items.set(item)
        order.save()
        # item.objects.status=True
        for item in item:
            item.status = True
            item.save()
        
        
        # item.delete()
        # return redirect('checkout')
        return render(request, 'checkout.html')

    except Exception as e:
        print(e)
        return redirect('home')


def search(request):
    query = request.GET.get('search')  
    if query:
        books = Book.objects.filter(title__icontains=query)  
    else:
        books = []  
    return render(request, 'search_results.html', {'books': books})


def book(request, book_id):
    book=Book.objects.filter(id=book_id)
    return render(request, 'Book.html', {'book': book})
    