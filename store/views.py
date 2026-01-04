from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
from .models import *
from django.utils import translation
from .utils import *

def custom_404(request, exception=None):
    return render(request, '404.html', status=404)

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)

    images = product.images.all()
    main_image = images.filter(is_main=True).first() or images.first()

    variants = product.variants.all()
    specs = product.specs.all()
    policy = getattr(product, 'policy', None)

    default_variant = (
        variants.filter(is_best_seller=True, is_available=True, inventory__gt=0).first()
        or variants.filter(is_available=True, inventory__gt=0).first()
        or variants.first()
    )
    for v in variants:
        v.display_price = format_usd(v.price)
        if v.old_price:
            v.display_old_price = format_usd(v.old_price)
    if default_variant:
        default_variant.display_price = format_usd(default_variant.price)
        if default_variant.old_price:
            default_variant.display_old_price = format_usd(default_variant.old_price)

    return render(request, 'products/detail.html', {
        'product': product,
        'images': images,
        'main_image': main_image,
        'variants': variants,
        'variant': default_variant,
        'specs': specs,
        'policy': policy,
    })





