from django import template
from home.models import *

register = template.Library()

# my custom filters


@register.filter
def doesfollow(value, arg):
    h=arg.follows.all()
    for obj in h:
        if str(obj)== value:
            return "Unfollow"

    return "Follow"


@register.filter
def sortfeed(value):
    res=[]
    for obj in value.follows.all():
        for pic in obj.following.photofeed.all():
            res.append(pic)

    for obj in value.photofeed.all():
        res.append(obj)

    res.sort(key=lambda x: x.dateTime, reverse=True)
    return res

@register.filter
def likepic(value, arg):
    a=Likes.objects.filter(user=value, feedmodel=arg)
    for obj in a:
        return 'home/images/hrt-full.png'
    return 'home/images/hrt.emp.png'