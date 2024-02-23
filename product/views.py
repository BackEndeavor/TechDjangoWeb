import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED

from product.models import Product
from product.serializers import ProductSerializer


@csrf_exempt
def product_create(request):
    if request.POST is None:
        return JsonResponse({'detail': f"Method \"{request.method}\" not allowed."}, status=HTTP_405_METHOD_NOT_ALLOWED)
    payload = json.loads(request.body)
    try:
        product = Product.objects.create(
            title=payload["title"],
            description=payload["description"],
            category=payload["category"],
            preview_image=payload["preview_image"],
            price=payload["price"]
        )
        serializer = ProductSerializer(product)
        return JsonResponse({"message": "Product created successfully", "product": serializer.data}, status=HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({"error": str(e)}, status=HTTP_404_NOT_FOUND)


@csrf_exempt
def product_read(request, product_id):
    if request.GET is None:
        return JsonResponse({'detail': f"Method \"{request.method}\" not allowed."}, status=HTTP_405_METHOD_NOT_ALLOWED)
    found_products = Product.objects.filter(id=product_id)
    serializer = ProductSerializer(found_products, many=True)
    return JsonResponse({"products": serializer.data}, status=HTTP_200_OK)


@csrf_exempt
def product_update(request):
    if request.POST is None:
        return JsonResponse({'detail': f"Method \"{request.method}\" not allowed."}, status=HTTP_405_METHOD_NOT_ALLOWED)
    payload = json.loads(request.body)
    try:
        found_product = Product.objects.filter(id=payload["id"])
        found_product.update(**payload)
        updated_product = Product.objects.filter(id=payload["id"])
        serializer = ProductSerializer(updated_product)
        return JsonResponse({"message": "Product updated successfully", "product": serializer.data}, status=HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({"error": str(e)}, status=HTTP_404_NOT_FOUND)


@csrf_exempt
def product_delete(request):
    if request.POST is None:
        return JsonResponse({'detail': f"Method \"{request.method}\" not allowed."}, status=HTTP_405_METHOD_NOT_ALLOWED)
    payload = json.loads(request.body)
    try:
        found_product = Product.objects.filter(id=payload["id"])
        found_product.delete()
        serializer = ProductSerializer(found_product)
        return JsonResponse({"message": "Product deleted successfully", "product": serializer.data}, status=HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({"error": str(e)}, status=HTTP_404_NOT_FOUND)
