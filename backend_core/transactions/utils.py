from datetime import datetime
from hashlib import md5


# status type
PENDING = 'PENDING'
FAIL = 'FAIL'
SUCCESS = 'SUCCESS'
ABORT = 'ABORT'
CANCEL = 'CANCEL'
TRANSACTION_STATUS_CHOICES = (
    (PENDING, 'Pending'),
    (FAIL, 'Fail'),
    (SUCCESS, 'Success'),
    (ABORT, 'Abort'),
    (CANCEL, 'Cancel'),
)


def generate_transaction_number(project_id):
    """

    :param project_id: current project id
    :type project_id: int

    :return: ret_md5: hashed MD5 with consumer, professional, project id and current time
    :type ret_md5: str
    """
    utc_time = int((datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0, 0)).total_seconds())
    m = md5.new('%d|%s' % (project_id, utc_time))
    return m.digest()
