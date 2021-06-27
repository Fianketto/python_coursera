from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def simple_route(request):
    if request.method == 'GET':
        return HttpResponse()
    else:
        resp = HttpResponse()
        resp.status_code = 405
        return resp


def slug_route(request):
    parts = request.path.split("/")
    return HttpResponse(parts[-2])


def sum_route(request):
    parts = request.path.split("/")
    res = str(int(parts[-2]) + int(parts[-3]))
    return HttpResponse(res)


@csrf_exempt
def sum_get_method(request):
    return get_sum(request, "GET", request.GET)


@csrf_exempt
def sum_post_method(request):
    return get_sum(request, "POST", request.POST)


def get_sum(request, method, method_params):
    if request.method == method:
        try:
            if len(method_params) == 2:
                s = 0
                for k in method_params:
                    s += int(method_params[k])
                resp = HttpResponse(str(s))
            else:
                resp = HttpResponse()
                resp.status_code = 400
        except:
            resp = HttpResponse()
            resp.status_code = 400
        return resp
    else:
        resp = HttpResponse()
        resp.status_code = 405
        return resp

