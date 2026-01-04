# orders/utils.py
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

def generate_invoice_pdf(order):
    html_string = render_to_string('orders/invoice.html', {'order': order})
    html = HTML(string=html_string)

    result = tempfile.NamedTemporaryFile(delete=True, suffix='.pdf')
    html.write_pdf(target=result.name)

    return result
