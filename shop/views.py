from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.http import HttpRequest, HttpResponse
from cart.forms import CartAddProductForm
from .recommender import Recommender

def product_list(request: HttpRequest, category_slug: str=None) -> HttpResponse:
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category, translations__language_code=language, translations__slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/products/list.html', dict(category=category, categories=categories, products=products))


def product_detail(request: HttpRequest, product_id: str, product_slug: str) -> HttpResponse:
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product, id=product_id,translations__language_code=language, translations__slug=product_slug, available=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(request, 'shop/products/detail.html', dict(product=product, cart_product_form=cart_product_form, recommended_products=recommended_products))

