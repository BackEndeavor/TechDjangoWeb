from django.views import generic

from product.models import Product


class IndexView(generic.ListView):
    model = Product
    template_name = 'index.html'
