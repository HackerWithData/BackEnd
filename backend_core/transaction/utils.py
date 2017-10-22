from datetime import datetime
from hashlib import md5


def generate_transaction_number(consumer_id, professional_id, project_id):
    """

    :param consumer_id: current consumer id
    :type consumer_id: int

    :param professional_id: selected professional id
    :type professional_id: int

    :param project_id: current project id
    :type project_id: int

    :return: ret_md5: hashed MD5 with consumer, professional, project id and current time
    :type ret_md5: str
    """
    utc_time = int((datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0, 0)).total_seconds())
    m = md5.new('%d|%d|%d|%s' % (consumer_id, professional_id, project_id, utc_time))
    return m.digest()
