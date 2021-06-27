'''
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'my_proj.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from my_app.models import User, Blog, Topic

u = User(first_name='Orkhan5', last_name='Hajili')
u.save()

u.name = 'Orkhan'
u.save()

# u.delete()
'''

dbg = False

if dbg:
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'my_proj.settings'
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

    from my_app.models import User, Blog, Topic
else:
    from db.models import User, Blog, Topic


import datetime
from django.db.models import Count, Avg
from django.db.models import Subquery


def create():
    # Создать пользователя first_name = u1, last_name = u1.
    user1 = User(first_name="u1", last_name="u1")
    user1.save()
    # Создать пользователя first_name = u2, last_name = u2.
    user2 = User(first_name="u2", last_name="u2")
    user2.save()
    # Создать пользователя first_name = u3, last_name = u3.
    user3 = User(first_name="u3", last_name="u3")
    user3.save()
    user1 = User.objects.filter(first_name='u1')[0]
    user2 = User.objects.filter(first_name='u2')[0]
    user3 = User.objects.filter(first_name='u3')[0]
    # Создать блог title = blog1, author = u1.
    blog1 = Blog(title="blog1", author=user1)
    blog1.save()
    # Создать блог title = blog2, author = u1.
    blog2 = Blog(title="blog2", author=user1)
    blog2.save()

    blog1 = Blog.objects.filter(title='blog1')[0]
    blog2 = Blog.objects.filter(title='blog2')[0]
    # Подписать пользователей u1 u2 на blog1, u2 на blog2.
    blog1.subscribers.add(user1, user2)
    blog1.save()
    blog2.subscribers.add(user2)
    blog2.save()
    # Создать топик title = topic1, blog = blog1, author = u1.
    topic1 = Topic(title="topic1", blog=blog1, author=user1)
    topic1.save()
    # Создать топик title = topic2_content, blog = blog1, author = u3, created = 2017 - 01 - 01.
    s = "2017-01-01 00:00:00"
    date_of_creation = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    if not dbg:
        topic2 = Topic(title="topic2_content", blog=blog1, author=user3, created=date_of_creation)
    else:
        topic2 = Topic(title="topic2_content", blog=blog1, author=user3)
    topic2.save()
    # Лайкнуть topic1 пользователями u1, u2, u3.
    topic1.likes.add(user1, user2, user3)
    topic1.save()


def edit_all():
    # Поменять first_name на uu1 у всех пользователей (функция edit_all).
    users = User.objects.all()
    for user in users:
        user.first_name = 'uu1'
        user.save()


def edit_u1_u2():
    # Поменять first_name на uu1 у пользователей, у которых first_name u1 или u2 (функция edit_u1_u2).
    users = User.objects.filter(first_name='u1') | User.objects.filter(first_name='u2')
    for user in users:
        user.first_name = 'uu1'
        user.save()


def delete_u1():
    # удалить пользователя с first_name u1
    users = User.objects.filter(first_name='u1')
    for i in range(len(users) - 1, -1, -1):
        user = users[i]
        user.delete()


def unsubscribe_u2_from_blogs():
    # отписать пользователя с first_name u2 от блогов
    blogs = Blog.objects.all()
    users = User.objects.filter(first_name='u2')
    for blog in blogs:
        try:
            blog.subscribers.remove(users[0])
        except:
            pass


def get_topic_created_grated():
    # Найти топики у которых дата создания больше 2018-01-01
    topics = Topic.objects.filter(created__gt="2018-01-01")
    return topics


def get_topic_title_ended():
    # Найти топик у которого title заканчивается на content
    topics = Topic.objects.filter(title__endswith="content")
    return topics


def get_user_with_limit():
    # Получить 2х первых пользователей (сортировка в обратном порядке по id) 
    users = User.objects.all().order_by("-id")[:2]
    return users


def get_topic_count():
    # Получить количество топиков в каждом блоге, назвать поле topic_count, отсортировать по topic_count по возрастанию
    query_set = Blog.objects.annotate(topic_count=Count('topic')).order_by('topic_count')
    #query_set = Blog.objects.annotate(topic_count=Count('topic')).values('topic_count').order_by('topic_count')
    #query_set = Topic.objects.values('blog_id').annotate(topic_count=Count('id')).order_by('topic_count')
    #query_set = Blog.objects.annotate(topic_count=Count('topic')).values('title', 'topic_count').order_by('topic_count')
    return query_set


def get_avg_topic_count():
    # Получить среднее количество топиков в блоге
    query_set = Blog.objects.annotate(topic_count=Count('topic')).aggregate(avg=Avg('topic_count'))
    return query_set



def get_blog_that_have_more_than_one_topic():
    # Найти блоги, в которых топиков больше одного
    query_set = Blog.objects.annotate(topic_count=Count('topic')).filter(topic_count__gt=0)
    return query_set


def get_topic_by_u1():
    # Получить все топики автора с first_name u1
    query_set = Topic.objects.filter(author_id__in=Subquery(User.objects.filter(first_name='u1').values('id')))
    return query_set


def get_user_that_dont_have_blog():
    # Найти пользователей, у которых нет блогов, отсортировать по возрастанию id
    #users = User.objects.annotate(blog_count=Count('blog')).filter(blog_count=1).values('id')
    #query_set = User.objects.filter(id__in=Subquery(users)).order_by('id')
    query_set = User.objects.annotate(blog_count=Count('blog')).filter(blog_count__lt=1).order_by('id')
    return query_set


def get_topic_that_like_all_users():
    # Найти топик, который лайкнули все пользователи
    user_count = User.objects.count()
    query_set = Topic.objects.annotate(all_likes=Count('likes')).filter(all_likes=user_count)
    return query_set


def get_topic_that_dont_have_like():
    # Найти топики, у которы нет лайков
    query_set = Topic.objects.annotate(all_likes=Count('likes')).filter(all_likes=0)
    return query_set
