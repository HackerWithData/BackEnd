from datetime import datetime
from Crypto.Hash import HMAC, MD5

from django.contrib.contenttypes.models import ContentType

from .models import Transaction, TransactionHistory
from users.models import CONSUMER, PROFESSIONAL
from projects.utils import get_a_uuid


def generate_transaction_number(project_id=None, milestone_id=None):
    """

    :param project_id: current project id
    :type project_id: int

    :return: ret_md5: hashed MD5 with consumer, professional, project id and current time
    :type ret_md5: str
    """
    if not project_id or not milestone_id:
        return None
    utc_time = int((datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0, 0)).total_seconds())
    h = HMAC.new(b'%d|%d|%s' % (project_id, milestone_id, utc_time))
    return h.hexdigest()


def get_transactions(user):
    if user.role == CONSUMER:
        transactions = Transaction.objects.filter(user=user)
        return transactions
    elif user.role == PROFESSIONAL:
        professional = user.professional_profiles.first().professional
        try:
            transactions = Transaction.objects.filter(professional=professional)
        except ContentType.DoesNotExist:
            return None
        return transactions


def get_or_create_transaction(**kwargs):
    transaction, created = Transaction.objects.get_or_create(**kwargs)
    return transaction, created


def generate_transaction_uuid():
    while True:
        uuid = get_a_uuid()
        try:
            Transaction.objects.get(uuid=uuid)
        except Transaction.DoesNotExist:
            break
    return uuid


def create_transaction_history(transaction):
    TransactionHistory.objects.create(transaction=transaction, status=transaction.status)

