from django.shortcuts import render,redirect,HttpResponse
from coverapp.models import Cover,Cart,Order
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q #
import random
import razorpay
from django.core.mail import send_mail
# Create your views here.
def AddCover(request):
    n="Iphone15"
    d="latest covers"
    p="500"
    c=Cover.objects.create(name=n,description=d,price=p)
    c.save()
    return HttpResponse("Cover Added !!")

def AboutUs(request):
    return render(request,'aboutus.html')


def home(request):
    context={}
    data = Cover.objects.all()
    context['covers']=data
    return render(request,'index.html',context)


def registerUser(request):
   if request.method =="GET":
      return render(request,'registration.html')
   else:      
      # 1. capture the values entered by user
      u = request.POST['username']
      if User.objects.filter(username=u).exists():
         context={'error':'Username already registered!! Please enter a different username for registration. '}
         return render(request,'registration.html',context)
      else:
         e = request.POST['email']
         p = request.POST['password']
         cp = request.POST['confirmpassword']
         # form validation
         if u=='' or e=='' or p=='' or cp=='':
            context={'error':'all fields are compulsory'}
            return render(request,'registration.html',context)
         elif p != cp :
            context={'error':'Pasword and Confirm Password must be same'}
            return render(request,'registration.html',context)
         else:
            #2.  insert in db
            # u = User.objects.create(username=u,password=p,email=e)
            # u.save()
            # above code will insert user details in table, but password is in plain text and not encrypted
            #use below code so as to encrypt the password, for security
            u = User.objects.create(username=u,email=e)
            u.set_password(p)# for password encryption
            u.save()  
            # context = {'success':'Registred successfully , plz login'} 
            messages.success(request,'Registered successfully, Please login')
            return redirect('/login')

def userLogin(request):
    if request.method == "GET":
        return render(request,'login.html')
    else:
        # Login Activity
        u = request.POST['username']
        p = request.POST['password']
        ur = authenticate(username=u, password=p)
        print(ur)
        if ur == None:
            context={'error':'Please provide correct details to login'}
            return render(request,'login.html',context)
        else:
            login(request,ur)
            return redirect("/")
        
def userLogout(request):
    logout(request)
    messages.success(request,'User Logged out successfully!')
    return redirect('/')

def addtocart(request,coverid):
    userid = request.user.id 
    if userid is None:
      context={'error':'Please login, so as to add your favourite Cover in your cart!!'}
      return render(request,'login.html',context)
    else:
      user = User.objects.get(id = userid)
      cover = Cover.objects.get(id=coverid) 
      cart = Cart.objects.create(uid=user, cid=cover)
      cart.save()
      messages.success(request,'Cover added to cart successfully !!')
      return redirect('showcart/')     


def showmycart(request):
    user = request.user
    cart=Cart.objects.filter(uid = user.id)
    TotalBill=0
    for cover in cart:
        TotalBill += cover.cid.price * cover.quantity
    count = len(cart)
    context={}
    context['cart']=cart
    context['total']=TotalBill
    context['count']=count
    return render(request,'showcart.html',context)

def removeCart(request,cartid):
    cart= Cart.objects.filter(id=cartid)
    cart.delete()
    messages.success(request,'Cover removed from cart!!')
    return redirect('removecover/')

def updateCart(request,opr,cartid):
    cart = Cart.objects.filter(id=cartid)
    if opr == '1':#opr is a string value [1]
        cart.update(quantity =cart[0].quantity + 1)
        return redirect('updatecart/')
    else: 
        cart.update(quantity =cart[0].quantity - 1)
        return redirect('updatecart/')

def searchByrange(request):
    min = request.GET['min']
    max = request.GET['max']
    c1 = Q(price__gte = min)
    c2 = Q(price__lte = max)
    coverList = Cover.objects.filter(c1 & c2)
    context={'covers':coverList}
    return render(request,'index.html',context)

def sortByprice(request,dir):
    col=''
    if dir == 'asc':
       col = 'price'
    else:
       col = '-price'
    coverList = Cover.objects.all().order_by(col)
    context={'covers':coverList}
    return render(request,'index.html',context)

def confirmOrder(request):
    user = request.user
    cart=Cart.objects.filter(uid = user.id)
    TotalBill=0
    for c in cart:
        TotalBill += c.cid.price * c.quantity
    count = len(cart)
    context={}
    context['cart']=cart
    context['total']=TotalBill
    context['count']=count
    return render(request,'confirmorder.html',context)

def makepayment(request):
    user=request.user
    usercart= Cart.objects.filter(uid = user.id)
    TotalBill=0
    for c in usercart:
        TotalBill += c.cid.price * c.quantity
    
    client = razorpay.Client(auth=("rzp_test_lQqNbmnLrTPgQl", "gkGZfEytQawMibc6LSSXXwr7"))
    data = { "amount": TotalBill*100, "currency": "INR", "receipt": "" }
    payment = client.order.create(data=data)
    context={'data':payment}
    print(payment)
    return render(request,'payment.html',context)

def placeOrder(request):
    #place order (insert order details in order table)
    user = request.user
    cart = Cart.objects.filter(uid=user.id)
    ordid = random.randrange(10000,99999)
    #verify if its not existing in database

    for c in cart:
        cover = Cover.objects.filter(id = c.cid.id)
        ord = Order.objects.create(uid=user[0],cid=cover[0],quantity = c.quantity, orderid = ordid)   
        ord.save()
        #clear cart
    cart.delete()
        #sending gmail

    msg_body = 'Order id is:'+str(ordid)
    custEmail = request.user.email
    send_mail( 
    "Order placed successfully!!", #subject
    msg_body, #message
    "dhanashreekorde29@gmail.com", #from
    [custEmail], #to
    fail_silently = False
    )

    messages.success(request,'Order placed successfully!!')
    return redirect('/')