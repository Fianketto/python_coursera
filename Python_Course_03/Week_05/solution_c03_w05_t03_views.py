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


from django.views.decorators.csrf import csrf_exempt
from django import forms

'''
import json
import base64
from functools import wraps
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django import forms
from .models import Item, Review
'''

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


def staff_required(view_func):
    """Декоратор проверяющший наличие флага is_staff у пользователя."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        response = HttpResponse(status=403)
        return response
    return _wrapped_view



class AddItemForm(forms.Form):
    title = forms.CharField(max_length=64, required=True, widget=forms.TextInput)
    description = forms.CharField(max_length=1024, required=True)
    price = forms.IntegerField(min_value=1, max_value=1000000, required=True)

    def clean(self):
        cleaned_data = super().clean()

        if not isinstance(self.data.get('title'), str):
            raise forms.ValidationError('The "title" field must be of type str.')

        if not isinstance(self.data.get('description'), str):
            raise forms.ValidationError('The "description" field must be of type str.')

        return cleaned_data


class AddReviewForm(forms.Form):
    text = forms.CharField(max_length=1024, required=True)
    grade = forms.IntegerField(min_value=1, max_value=10, required=True)

    def clean(self):
        cleaned_data = super().clean()

        if not isinstance(self.data.get('text'), str):
            raise forms.ValidationError('The "text" field must be of type str.')

        return cleaned_data


@method_decorator(basicauth, name='dispatch')
@method_decorator(staff_required, name='dispatch')
class AddItemView(View):

    def post(self, request):

        try:
            form = AddItemForm(json.loads(request.body))
        except json.JSONDecodeError:
            return HttpResponse(status=400)

        if not form.is_valid():
            return HttpResponse(status=400)

        new_item = Item(title=form.cleaned_data['title'],
                        description=form.cleaned_data['description'],
                        price=form.cleaned_data['price'])
        new_item.save()
        return JsonResponse({'id': new_item.id}, status=201, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):

    def post(self, request, item_id):

        try:
            form = AddReviewForm(json.loads(request.body))
        except json.JSONDecodeError:
            return HttpResponse(status=400)

        if not form.is_valid():
            return HttpResponse(status=400)

        if not Item.objects.filter(pk=item_id).exists():
            return HttpResponse(status=404)

        review = Review(
            text=form.cleaned_data['text'],
            grade=form.cleaned_data['grade'],
            item_id=item_id
        )
        review.save()
        return JsonResponse({'id': review.id}, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class GetItemView(View):

    def get(self, request, item_id):

        if not Item.objects.filter(pk=item_id).exists():
            return HttpResponse(status=404)

        item_data = Item.objects.filter(pk=item_id).first()
        item_reviews = Review.objects.filter(item=item_id).order_by('-id')[:5]
        reviews = []

        for review in item_reviews:
            reviews.append({'id': review.id, 'text': review.text, 'grade': review.grade})

        result = {
            'id': item_id,
            'title': item_data.title,
            'description': item_data.description,
            'price': item_data.price,
            'reviews': reviews
        }
        return JsonResponse(result, status=200)
