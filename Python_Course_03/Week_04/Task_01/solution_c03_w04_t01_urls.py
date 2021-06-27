from django.contrib import admin
from django.conf.urls import url
from .views import *


urlpatterns = [
    url('^simple_route/$', simple_route),
    url('^slug_route/[a-z0-9-_]{1,16}/$', slug_route),
    url('^sum_route/-?[1-9][0-9]*/-?[1-9][0-9]*/$', sum_route),
    url('^sum_get_method/$', sum_get_method),
    url('^sum_post_method/$', sum_post_method),
    url('admin/', admin.site.urls),
]
