from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def echo(request):
    res = ''
    if request.method == 'GET':
        if len(request.GET) > 0:
            res += f"get "
            for k, v in request.GET.items():
                res += f"{k}: {v} "
    elif request.method == 'POST':
        if len(request.POST) > 0:
            res += f"post "
            for k, v in request.POST.items():
                res += f"{k}: {v} "

    res += "statement is "
    txt = request.META.get('HTTP_X_PRINT_STATEMENT', '')
    if txt == '':
        txt = 'empty'
    res += txt
    return HttpResponse(res)


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })
