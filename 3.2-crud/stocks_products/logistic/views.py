from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    # при необходимости добавьте параметры фильтрации

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')

        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        product_id = instance.id
        product_title = instance.title
        self.perform_destroy(instance)
        return Response(
            {"message": f"Продукт {product_title} с id={product_id} успешно удален"},
            status=status.HTTP_200_OK
        )


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    # при необходимости добавьте параметры фильтрации

    def get_queryset(self):
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('products')
        search_query = self.request.query_params.get('search')

        # Фильтрация по ID продукта
        if product_id:
            queryset = queryset.filter(
                positions__product_id=product_id
            ).distinct()

        # Фильтрация по названию/описанию продукта
        elif search_query:
            matching_products = Product.objects.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

            queryset = queryset.filter(
                positions__product__in=matching_products
            ).distinct()

        queryset = queryset.prefetch_related(
            'positions',
            'positions__product'
        )

        return queryset
