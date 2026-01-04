# orders/emails.py
from django.core.mail import EmailMessage
from .utils import generate_invoice_pdf

def send_invoice_email(order):
    pdf = generate_invoice_pdf(order)

    email = EmailMessage(
        subject=f'Your Invoice #{order.id}',
        body='Thank you for your purchase. Invoice attached.',
        to=[order.email]
    )

    email.attach(f'invoice_{order.id}.pdf', pdf.read(), 'application/pdf')
    email.send()
