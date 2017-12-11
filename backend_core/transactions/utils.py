from datetime import datetime
from hashlib import md5
from Crypto.Hash import HMAC, MD5


# status type
PENDING = 'P'
FAIL = 'F'
SUCCESS = 'S'
ABORT = 'A'
CANCEL = 'C'
TRANSACTION_STATUS_CHOICES = (
    (PENDING, 'PENDING'),
    (FAIL, 'FAILED'),
    (SUCCESS, 'SUCCESS'),
    (ABORT, 'ABORTED'),
    (CANCEL, 'CANCELED'),
)


def generate_transaction_number(project_id, milestone_id):
    """

    :param project_id: current project id
    :type project_id: int

    :return: ret_md5: hashed MD5 with consumer, professional, project id and current time
    :type ret_md5: str
    """
    utc_time = int((datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0, 0)).total_seconds())
    h = HMAC.new(b'%d|%d|%s' % (project_id,milestone_id, utc_time))
    return h.hexdigest()
