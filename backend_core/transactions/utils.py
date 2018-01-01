from datetime import datetime
from hashlib import md5
from Crypto.Hash import HMAC, MD5

from .models import Transaction, TransactionHistory
from users.utils import CONSUMER, PROFESSIONAL
from projects.utils import get_a_uuid


def generate_transaction_number(project_id, milestone_id):
    """

    :param project_id: current project id
    :type project_id: int

    :return: ret_md5: hashed MD5 with consumer, professional, project id and current time
    :type ret_md5: str
    """
    utc_time = int((datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0, 0)).total_seconds())
    h = HMAC.new(b'%d|%d|%s' % (project_id, milestone_id, utc_time))
    return h.hexdigest()


def get_transactions(user):
    if user.role == CONSUMER:
        transactions = Transaction.objects.filter(user=user)
        return transactions
    elif user.role == PROFESSIONAL:
        professional = user.professional_profiles.first().professional
        transactions = Transaction.objects.filter(
            content_type=ContentType.objects.get(model=professional.type.lower()),
            object_id=int(professional.lic_num)
        )
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

