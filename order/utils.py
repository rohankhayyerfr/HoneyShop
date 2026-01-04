from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_invoice_email(order):
    subject = f"فاکتور سفارش #{order.id}"
    to_email = order.email

    html_content = render_to_string(
        "orders/invoice.html",
        {"order": order}
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body="فاکتور سفارش شما",
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
