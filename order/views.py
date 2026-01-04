from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from .email_utils import send_invoice_email
from HoneyShop import settings
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from .paypal import paypal_client
from django.http import JsonResponse


def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/payment.html', {
        'order': order,
        'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID,
    })

def checkout(request):
    global order
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session = request.session.session_key
        cart = Cart.objects.filter(session_id=session).first()

    if not cart or not cart.items.exists():
        return redirect('store:product_list')

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_id=request.session.session_key,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            total_price=cart.final_total
        )

        for item in cart.items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variant=item.variant,
                quantity=item.quantity,
                price=item.unit_price
            )



        return redirect('payment', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart': cart})


def create_paypal_order(request, order_id):
    order = Order.objects.get(id=order_id)
    request_paypal = OrdersCreateRequest()
    request_paypal.prefer("return=representation")
    request_paypal.request_body({
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": settings.PAYPAL_CURRENCY,
                "value": str(order.total_price)  # حتما string و بدون کاما
            }
        }]
    })
    response = paypal_client().execute(request_paypal)
    return JsonResponse({"id": response.result.id})



@csrf_exempt
def capture_paypal_order(request, order_id):
    if request.method != "POST":
        return JsonResponse({"success": False}, status=400)

    paypal_order_id = request.POST.get("paypal_order_id")
    order = Order.objects.get(id=order_id)

    from .paypal import paypal_client
    request_capture = OrdersCaptureRequest(paypal_order_id)
    response = paypal_client().execute(request_capture)

    if response.result.status == "COMPLETED":
        order.status = "paid"
        order.save()
        send_invoice_email(order)
        return JsonResponse({"success": True}, status=200)

    return JsonResponse({"success": False}, status=400)


def payment_success(request):
    return render(request, 'orders/payment_success.html')

def payment_failed(request):
    return render(request, 'orders/payment_failed.html')