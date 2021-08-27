from django.shortcuts import render, get_object_or_404
from .models import Category, Product
#from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wishlist.models import Wishlist, WishlistItem
from django.contrib.postgres.search import SearchVector


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)

        products = products.filter(category=category)
    page = request.GET.get('page')
    paginator = Paginator(products, 6)
    try:
        products = paginator.page(page)

    except PageNotAnInteger:
        products = paginator.page(1)

    except EmptyPage:
        products = paginator.page(1)

    if request.user.username:
        wishlist = Wishlist.objects.filter(user=request.user)

        return render(request, 'shop/product/list.html', {'category': category, 'categories': categories, 'products': products, 'wishlist': wishlist})

    else:
        return render(request, 'shop/product/list.html', {'category': category,
                                                          'categories': categories,
                                                          'products': products, })


def product_search(request):
    results = None
    try:
        query = request.POST['query']
        results = Product.objects.filter(name__icontains=query) |\
            Product.objects.filter(description__icontains=query)
        page = request.GET.get('page')
        paginator = Paginator(results, 6)
        try:
            results = paginator.page(page)

        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:

            results = paginator.page(1)
        category = None
        categories = None
        wishlist = None
        return render(request, 'shop/product/list.html', {'products': results, 'wishlist': wishlist})
    except KeyError:
        category = None
        categories = None
        wishlist = None
        "KeyError"
        return render(request, 'shop/product/list.html', {'products': results, 'wishlist': wishlist})
        


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    #cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   })  # 'cart_product_form': cart_product_form
