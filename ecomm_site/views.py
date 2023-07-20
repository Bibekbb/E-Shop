from django.shortcuts import  render, redirect, HttpResponse
from app.models import  Category, SubCategory, Product, Contact_us, Order, Brand
from django.contrib.auth import authenticate,login
from app.forms import UserCreationForm
from app.models import  User
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib.auth.models import User
from sklearn.neighbors import KNeighborsClassifier
import numpy as np




def base(request):
    return render(request, 'base.html')



def index(request):
    category = Category.objects.all()
    product = Product.objects.all()
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')
    categoryID = request.GET.get('category')


    if categoryID:
        product = Product.objects.filter(subcategory = categoryID).order_by('-id')
    elif brandID:
        product = Product.objects.filter(brand = brandID).order_by('-id')
    else:
        product = Product.objects.all()



    # if categoryID:
    #     product = Product.objects.filter(subcategory = categoryID).order_by('-id')
    # else:
    #     product = Product.objects.all()


    context = {
        'category':category,
        'product':product,
        'brand':brand,
    }
    return  render(request,'index.html',context)



def SignUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
            )
            login(request, new_user)
            return redirect('index')
    else:
        form = UserCreationForm()
    context={
        'form':form
    }
    return render(request, 'registration/signup.html', context)


@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')



def contact_page(request):
    if request.method == 'POST':
        contact = Contact_us(
            name = request.post.get('name'),
            email = request.post.get('email'),
            subject = request.post.get('subject'),
            message = request.post.get('message'),
        )
        contact.save()

    return render(request, 'contact/contact.html')


def CheckOut(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        zipcode = request.POST.get('zipcode')
        cart = request.session.get('cart')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk=uid)
        print(cart)
        for i in cart:
            a = cart[i]['price']
            b = cart[i]['quantity']
            total = a*b
            order = Order(
                user = user,
            product = cart[i]['name'],
            price = cart[i]['price'],
            quantity = cart[i]['quantity'],
            image = cart[i]['image'],
            address = address,
            phone = phone,
            zipcode = zipcode,
            total = total,
            )
            order.save()
        request.session['cart'] = {}
        return redirect('index')
    
   

    return HttpResponse("This is the checkout Page")



def YourOrder(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    order = Order.objects.filter(user=user)
    context = {
        'order':order
    }
    return render(request, 'order.html', context)


def Product_Page(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')
    categoryID = request.GET.get('category')


    if categoryID:
        product = Product.objects.filter(subcategory = categoryID).order_by('-id')
    elif brandID:
        product = Product.objects.filter(brand = brandID).order_by('-id')
    else:
        product = Product.objects.all()


    context ={
        'category':category,
        'brand':brand,
        'product':product,
    }
    return render(request, 'product.html', context)




def Product_Detail(request,id):
    product = Product.objects.filter(id = id).first()
    context = {
        'product':product,
    }

    return render(request, 'product_detail.html',context)



def Search(request):
    query = request.GET['query']
    product = Product.objects.filter(name__icontains=query)
    context = {
        'product':product,
    }
    return render(request, 'search.html', context)


#Trainning data
X_train = np.array([[0, 1, 0, 1],
                    [1, 0, 1, 0],
                    [0, 0, 1, 1],
                    [1, 0, 0, 0]])

Y_train = np.array(['Outfit 1', 'Outfit 2', 'Outfit 3', 'Outfit 4'])

#Train Knn model
knn_model = KNeighborsClassifier(n_neighbors=3)
knn_model.fit(X_train, Y_train)

def preprocess_input(user_input):
    #Preprocess user input and convert it to features vector
    color = 1 if user_input['color'] == 'blue' else 0
    style = 1 if user_input['style'] == 'formal' else 0
    occasion = 1 if user_input['occasion'] == 'formal' else 0
    season = 1 if user_input['season'] == 'summer' else 0

    return [color, style, occasion, season]


def get_outfits_by_indices(indices):
    # Retrieve outfit recommendations based on indices
    outfits = ['Outfit 1', 'Outfit 2', 'Outfit 3', 'Outfit 4']
    recommendations = [outfits[i] for i in indices]

    return recommendations



def outfit_recommendation(request):
    if request.method == 'POST':
        user_input = {
            'color': request.POST['color'],
            'style': request.POST['style'],
            'occasion': request.POST['occasion'],
            'season': request.POST['season']
        }

        input_features = preprocess_input(user_input)
        input_features = np.array(input_features).reshape(1, -1)  # Reshape input features

        _, indices = knn_model.kneighbors(input_features, n_neighbors=3)  # Use knn_model directly

        recommendations = get_outfits_by_indices(indices[0])  # Retrieve recommendations

        context = {'recommendations': recommendations}
        return render(request, 'outfit_recommendation.html', context)

    return render(request, 'input_form.html')
