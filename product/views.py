import json
from tempfile import NamedTemporaryFile

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED, HTTP_409_CONFLICT

from product.models import Product
from product.serializers import ProductSerializer


@csrf_exempt
def product_create(request):
    if request.POST is None:
        return JsonResponse({'detail': f"Method \"{request.method}\" not allowed."}, status=HTTP_405_METHOD_NOT_ALLOWED)
    payload = json.loads(request.body)
    try:
        title = payload["title"]
        if Product.objects.filter(title=title).exists():
            return JsonResponse({'detail': f"Product with title \"{title}\" already exists"}, status=HTTP_409_CONFLICT)
        # We are using such hacky way to download image files if preview_image provided link is image
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(requests.get(payload["preview_image"]).content)
        img_temp.flush()
        product = Product.objects.create(
            title=title,
            description=payload["description"],
            category=payload["category"],
            preview_image=title,
            price=payload["price"]
        )
        with open(img_temp.name, 'rb') as src, open(product.preview_image.path, 'wb') as dst:
            dst.write(src.read())
        img_temp.close()
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
