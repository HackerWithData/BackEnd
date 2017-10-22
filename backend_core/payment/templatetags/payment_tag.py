from django import template
from django.conf import settings
from hashlib import md5
from datetime import datetime

register = template.Library()


@register.inclusion_tag('payment/pay_now_button.html', takes_context=True)
def render_pay_now_button(context, total_amount, order_number):
    """

    :param context: context parameter, don't need to pass in manually
    :type context: dict

    :param total_amount: total amount need to be charged
    :type total_amount: float

    :param order_number: payment object primary key
    :type order_number: int

    :return: rendered payment button element
    :type: dict
    """
    ret = settings.FORTE_CONFIG.copy()
    ret['total_amount'] = total_amount
    ret['order_number'] = order_number
    ret['utc_time'] = int((datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0, 0)).total_seconds())
    # no customer_token and paymehtod_token
    # string eg.   api_login_id | method | version_number | total_amount | utc_time | order_number | customer_token | paymethod_token
    m = md5.new('%s|%s|%s|%f|%d|%d||' % (ret['api_login_id'],
                                         ret['method'],
                                         ret['version_number'],
                                         total_amount,
                                         ret['utc_time'],
                                         order_number))
    ret['signature'] = m.digest()
    return ret
