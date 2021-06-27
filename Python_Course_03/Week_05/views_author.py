import base64
import json

from functools import wraps
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate

from django.http import HttpResponse, JsonResponse
from django.views import View

from .models import Item, Review

from jsonschema import validate
from jsonschema.exceptions import ValidationError


ADDITEM_SCHEMA = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'title':{
            'type': 'string',
            'minLength': 1,
            'maxLength': 64,
        },
        'description': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 1024,
        },
        'price': {
            'type': ['string', 'integer'],
            'minimum': 1,
            'maximum': 1000000,
            'minLength': 1,
            'maxLength': 7,
            'pattern': r'^[^0]\d*$',
            }
    },
    'required': ['title', 'description', 'price'],    
}

POSTREVIEW_SCHEMA = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'text':{
            'type': 'string',
            'minLength': 1,
            'maxLength': 1024,
        },
        'grade': {
            'type': ['string', 'integer'],
            'minimum': 1,
            'maximum': 10,
            'minLength': 1,
            'maxLength': 2,
            'pattern': r'^[^0]\d*$',
            }
    },
    'required': ['text', 'grade'],    
}


#Для реализации HTTP Basic Auth в фреймворке Django обычно используются middleware
#или реализуется auth backend 
#https://docs.djangoproject.com/en/dev/topics/auth/customizing/
#Но в данном случае так как весь код должен располагаться в файле views.py лучше
# реализовать аутентификацию на базе декоратора для view:
def basicauth(view_func):
    """Декоратор реализующий HTTP Basic AUTH."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == 'basic':
                    token = base64.b64decode(auth[1].encode('ascii'))
                    username, password = token.decode('utf-8').split(':')
                    user = authenticate(username=username, password=password)
                    if user is not None and user.is_active:
                        request.user = user
                        return view_func(request, *args, **kwargs)

        response = HttpResponse(status=401)
        response['WWW-Authenticate'] = 'Basic realm="Somemart staff API"'
        return response
    return _wrapped_view


#Декоратор выполняет аутентификацию пользователя используя стандартный метод authenticate
#из пакета django.contrib.auth. Также в задании указано, что помимо того что пользователь 
#должен быть аутентифицирован, у пользователя должен быть проставлен флаг is_staff. 
#В нашем случае мог бы подойти декоратор staff_member_required, но так как у нас API и мы
#не хотим осуществлять редирект на страницу логина, то стоит реализовать свой декоратор.
def staff_required(view_func):
    """Декоратор проверяющший наличие флага is_staff у пользователя."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        response = HttpResponse(status=403)
        return response
    return _wrapped_view         


#Теперь остается только подключить декораторы к View.
@method_decorator(basicauth, name='dispatch')
@method_decorator(staff_required, name='dispatch')
class AddItemView(View):
    """View для создания товара."""
    
    def post(self, request):
        try:            
            document = json.loads(request.body)
            validate(document, ADDITEM_SCHEMA)
            item = Item.objects.create(
                title=document.get("title"),
                description=document.get("description"),
                price=document.get("price")
            )
            data = {"id": item.id}
            return JsonResponse(data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'errors':'запрос не прошел валидацию'}, status=400)
        except ValidationError:
            return JsonResponse({'errors':'запрос не прошел валидацию'}, status=400)


class PostReviewView(View):
    """View для создания отзыва о товаре."""
    def post(self, request, item_id):
        try:
            document = json.loads(request.body)
            validate(document, POSTREVIEW_SCHEMA)
            item = Item.objects.get(pk=item_id)
            review = Review.objects.create(
                grade=document.get('grade'),
                text=document.get('text'),
                item=item
            )
            data = {"id": review.id}
            return JsonResponse(data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'errors':'запрос не прошел валидацию'}, status=400)
        except ValidationError:
            return JsonResponse({'errors':'запрос не прошел валидацию'}, status=400)
        except Item.DoesNotExist:
            return HttpResponse(status=404)

            
class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        item = Item.objects.filter(pk=item_id)
        reviews = Review.objects.filter(item__pk=item_id).order_by('-pk')[:5]
        if item:
            data = {
                "id": item[0].id,
                "title": item[0].title,
                "description": item[0].description,
                "price": item[0].price,
                "reviews": [{
                    "id": review.id,
                    "text": review.text,
                    "grade": review.grade
                } for review in reviews]
            }
            return JsonResponse(data, status=200)
        else:
            return HttpResponse(status=404)
