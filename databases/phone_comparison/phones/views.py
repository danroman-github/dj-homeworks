from django.shortcuts import render, get_object_or_404
from phones.models import Phone


def show_catalog(request):
    sort = request.GET.get('sort', 'name')

    sort_mapping = {
        'name': 'name',
        'min_price': 'price',
        'max_price': '-price'
    }

    order_by = sort_mapping.get(sort, 'name')

    template = 'catalog.html'
    phones = Phone.objects.all().order_by(order_by)
    context = {
        'phones': phones
    }
    return render(
        request,
        template,
        context
    )

def product_detail(request, slug):
    phone = get_object_or_404(Phone, slug=slug)
    return render(request, 'product.html', {'phone': phone})
