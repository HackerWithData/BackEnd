from django import template
from django.conf import settings
from Crypto.Hash import HMAC, MD5
from datetime import datetime

from ..utils import generate_transaction_number
from projects.models import Project, Milestone

register = template.Library()


@register.inclusion_tag('payment/pay_now_button.html', takes_context=True)
def render_pay_now_button(context, project_uuid, milestone_uuid):
    """

    :param context: context parameter, don't need to pass in manually
    :type context: dict

    :param project_id: current project id
    :type project_id: int

    # :param total_amount: total amount need to be charged
    # :type total_amount: float

    # :param order_number: payment object primary key
    # :type order_number: int

    :return: rendered payment button element
    :type: dict
    """
    ret = settings.FORTE_CONFIG.copy()
    del ret['secure_trans_key']
    project_id = Project.objects.get(uuid=project_uuid).pk
    milestone_id = Milestone.objects.get(uuid=milestone_uuid).pk
    ret['project_uuid'] = project_uuid
    ret['total_amount'] = Milestone.objects.get(uuid=milestone_uuid).amount
    ret['milestone_uuid'] = milestone_uuid
    ret['order_number'] = generate_transaction_number(project_id,milestone_id)
    ret['utc_time'] = int((datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0, 0)).total_seconds())
    # no customer_token and paymehtod_token
    # string eg.   api_login_id | method | version_number | total_amount | utc_time | order_number | customer_token | paymethod_token
    secret = b"%s|%s|%s|%s|%d|%s||" % (ret['api_login_id'],
                                       ret['method'],
                                       ret['version_number'],
                                       ret['total_amount'],
                                       ret['utc_time'],
                                       ret['order_number'])
    h = HMAC.new(key=str(settings.FORTE_CONFIG['secure_trans_key']), msg=str(secret), digestmod=MD5)

    # h.update(settings.FORTE_CONFIG['secure_trans_key'])
    ret['signature'] = h.hexdigest()
    # print ret['signature']


    return ret
