import re
import random

from django import template
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
import os
from core.utils.text import to_consize_digits
from core.utils.core import get_file_type
register = template.Library()


@register.filter
def make_int_iterable(number):
    return range(number)

@register.filter
def complete_rating_stars_iter(rating) :
    diff = 5 - rating
    if diff <= 0 :
        diff = 0
    return range(diff)    

@register.filter(name='intdivide')
def intdivide(value, div):
    try:
        return int(value)//int(div)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter
def beginswith(text, test):
    try:
        return str(text.__str__()).startswith(str(test))

    except:
        return False


@register.filter
def startswith(text, test):
    try:
        return text.startswith(test)

    except:
        return False


@register.filter
def if_empty(text, default):
    try:
        if len(str(text)) < 1 or text == "None" or not text:
            return default
        else:
            return text
    except:
        return default


@register.filter
def readtime(text):

    try:
        read_speed = 150
        count = len(str(text.split()))
        time = count//read_speed
        if time < 1:
            time = 1
        return time
    except ValueError:
        return None


@register.filter
def file_type(file_path):
    """ returns if video or image """
    return get_file_type(file_path)


@register.filter
def readable(text):
    try:
        text = str(text)
        text = text.split('_')
        text = ' '.join(text)
        return text

    except ValueError:
        return None


@register.filter
def upper(text):
    try:

        return str(text).upper()

    except ValueError:
        return None


@register.filter
def capitalize(text):
    try:

        return str(text).capitalize()

    except ValueError:
        return None


@register.filter
def time_published_verbose(date):

    current = timezone.now()
    diff = current - date
    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
        seconds = diff.seconds
        if seconds == 0:
            return "now"
        elif seconds == 1:
            return str(seconds) + "s"
        else:
            return str(seconds) + "s"

    if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
        if diff.seconds < 120:
            return str(diff.seconds//60) + "m"
        else:
            return str(diff.seconds//60) + "m"

    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
        if diff.seconds < 7200:
            return str(diff.seconds//3600) + "h"
        else:
            return str(diff.seconds//3600) + "h"

    if diff.days >= 1 and diff.days < 30:
        if diff.days < 2:
            return str(1) + "d"
        else:
            return str(diff.days) + "d"

    if diff.days >= 30 and diff.days < 365:
        if diff.days < 60:
            return str(diff.days//30) + "m"
        else:
            return str(diff.days//30) + "m"

    if diff.days >= 365:
        if diff.days < 730:
            return str(diff.days//365) + "y"
        else:
            return str(diff.days//365) + "y"


@register.filter
def frontspace(txt):
    try:
        return str(txt) + "    ."
    except ValueError:
        return None


@register.filter
def backspace(txt):
    try:
        return "  " + str(txt)
    except ValueError:
        return None


@register.filter
def few_letter(txt, letters):
    cut_out = txt[:int(letters)]
    return cut_out + ".." if len(cut_out) < len(txt) else cut_out


@register.filter
def fewwords(txt, words):
    if len(txt) == 0:
        return ""
    try:

        words = int(words)
        text = txt.split()
        if len(text) > words:
            txt = text[:words]
            txt = " ".join(txt)
            txt = txt + "..."
        return str(txt)
    except ValueError:
        return None


@register.filter
def attr(dict, key):
    try:
        return dict.get(key)
    except ValueError:
        return None


@register.filter(name='get_attr')
def get_attr(instance, attr_name):
    """Get an attribute of an instance dynamically."""
    if hasattr(instance, attr_name):
        return getattr(instance, attr_name)
    return None


@register.filter(name='get_verbose')
def get_verbose(text):
    """turn any string to verbose"""
    try : str(text)
    except : return None
    return " ".join(text.split("_")) 


@register.filter
def boldmentions(text):
    new_text = format_html("")
    validate = URLValidator()
    from django.core.validators import URLValidator
    from django.core.exceptions import ValidationError

    try:
        words = text.split()
        for word in words:
            try:
                validate(word)
                new_text = new_text + format_html(
                    " <a style='color:#046fad' href ='{}'><strong>{}</strong></a>",
                    word,
                    word
                )
                # if theres a match, move to the next
                continue
            except:
                pass
            if word.startswith('@'):
                # verifying the username
                try:
                    profile_link = reverse("profile", args=[word.strip('@')])
                    new_text = new_text + format_html(
                        " <a style='color:#046fad' href ='{}'><strong>{}</strong></a>",
                        profile_link,
                        word
                    )

                except:
                    # render normally

                    new_text = new_text + format_html(" {}", word)

            elif word.startswith('#'):
                try:
                    url = reverse("explore-tag", args=[word.strip("#")])
                    new_text = new_text + format_html(
                        " <a href = '{}' style ='color:#046fad'><strong>{}</strong></a>",
                        url, word
                    )

                except:
                    new_text = new_text + format_html(" {}", word)

            else:
                new_text = new_text + format_html(" {}", word)

        return new_text

    except TypeError:
        return ""


@register.filter
def contains(text, word):
    try:
        if word in text:
            return True
        else:
            return False
    except:
        return None


@register.filter
def subtract(num):
    try:
        return int(num) - 1
    except:
        return num


@register.filter
def social_post_comments_no(post):
    no = 0
    try:
        for comment in post.social_post_comment.all():
            if not comment.parent_comment:
                no += 1
        return no
    except AttributeError:
        return None


@register.filter
def make_iterable(obj):
    # converts a single object to an itrable, list of just one item
    return [obj]


@register.filter
def consize_digit(number, control=None):
    if control == "hide_if_zero":
        if number == 0:
            return ""
    """ turns 10453 to 10.4k 1223343 to 1.2M etc"""
    return to_consize_digits(number)


@register.filter
def shuffle(_list):
    try:
        random.shuffle(_list)
        random.shuffle(_list)
    except:
        pass
    return _list


@register.filter
def list_as_text(_list):
    # stringify all components
    return ", ".join([str(member) for member in _list])


@register.filter
def convert_currency(amount,_to) :
    #taking into assumption that defualt is USD
    from core.functions import convert_currency
    #returns a tuple of currency html value and price
    try :
        new_price = convert_currency(amount,"USD",_to)
    except TypeError :
        return amount    
    return new_price

    