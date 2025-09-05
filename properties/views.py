from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from .models import Property
from .utils import get_all_properties


@csrf_exempt
@cache_page(60 * 15)
def property_list(request):
    properties = get_all_properties()
    return JsonResponse({'data': list(properties)}, safe=False)
