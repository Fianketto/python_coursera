import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Item, Review


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""
    def post(self, request):
        valid = True
        title = description = price = None
        '''
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        price = request.POST.get('price', 0)
        '''
        try:
            body_unicode = request.body.decode('utf-8')
            post_data = json.loads(body_unicode)

            title = post_data.get('title', '')
            description = post_data.get('description', '')
            price = post_data.get('price', 0)
        except:
            valid = False

        if not isinstance(title, str) or len(title) < 1 or len(title) > 64:
            valid = False
        if not isinstance(description, str) or len(description) < 1 or len(description) > 1024:
            valid = False
        try:
            price = int(price)
            if price < 1 or price > 1000000:
                valid = False
        except:
            valid = False

        if valid:
            good_count = Item.objects.count() + 1

            new_good = Item(title=title, description=description, price=price)
            new_good.save()

            data = {"id": good_count}
            status_code = 201
        else:
            data = {}
            status_code = 400

        return JsonResponse(data, status=status_code)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""
    def post(self, request, item_id):
        valid = True
        text = grade = None
        '''
        text = request.POST.get('text', '')
        grade = request.POST.get('grade', 0)
        '''
        try:
            body_unicode = request.body.decode('utf-8')
            post_data = json.loads(body_unicode)

            text = post_data.get('text', '')
            grade = post_data.get('grade', 0)
        except:
            valid = False

        if not isinstance(text, str) or len(text) < 1 or len(text) > 1024:
            valid = False
        try:
            grade = int(grade)
            if grade < 1 or grade > 10:
                valid = False
        except:
            valid = False

        good_count = Item.objects.count()
        review_count = Review.objects.count()

        if int(item_id) > good_count:
            data = {}
            status_code = 404
        elif valid:
            review_count += 1
            this_good = Item.objects.filter(id=item_id)[0]
            new_review = Review(text=text, grade=grade, item=this_good)
            new_review.save()

            data = {"id": review_count}
            status_code = 201
        else:
            data = {}
            status_code = 400


        return JsonResponse(data, status=status_code)


@method_decorator(csrf_exempt, name='dispatch')
class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """
    def get(self, request, item_id):
        good_id = int(item_id)
        good_count = Item.objects.count()
        review_count = Review.objects.count()
        if good_id > good_count:
            data = {}
            status_code = 404
        else:

            item = Item.objects.filter(id=good_id)[0]
            revs = Review.objects.filter(item=item).order_by('-id')[:5]
            item_count = Item.objects.count()
            rev_count = Review.objects.count()
            reviews = []
            for r in revs:
                reviews.append({'id': r.id, 'text': r.text, 'grade': r.grade})

            data = {
                    'id': good_id,
                    'title': item.title,
                    'description': item.description,
                    'price': item.price,
                    'reviews': reviews
                }
            status_code = 200
            
        return JsonResponse(data, status=status_code)
