from django import template
import datetime

register = template.Library()


@register.filter(name='timestamp_to_time')
def convert_timestamp_to_time(timestamp):
    return datetime.date.fromtimestamp(int(timestamp))
