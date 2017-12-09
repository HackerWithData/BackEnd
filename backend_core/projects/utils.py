import uuid
from django.utils.translation import ugettext_lazy as __
from django.contrib.contenttypes.models import ContentType

WAITING = "W"
PAID_TO_HOOME = "PTH"
PAID_TO_PROFESSIONAL = "PTP"

PAYMENT_REQUEST = 'M'

WAITING_ACTION = "Contractor is waiting for the payment"

PENDING = 'P'
ACCEPTED = 'A'
REJECTED = 'R'
ONGOING = "O"
DONE = "D"
# TODO: need to move sucess to transaction.utils
# WITHDRAWN = "Withdrawn"
# RETURNED = "Returned"
# SUCCESS = "Success"

MILESTONE_STATUS = (
    (WAITING, __("Waiting")),
    (PAID_TO_HOOME, __("Paid to Hoome")),
    (PAID_TO_PROFESSIONAL, __("Paid to Professional")),
    (DONE, __("Done")),
    (PAYMENT_REQUEST, __("Payment Request")),
)

PROJECT_STATUS = (
    (PENDING, __('PENDING')),
    (ACCEPTED, __('ACCEPTED')),
    (ONGOING, __('ONGOING')),
    (REJECTED, __('REJECTED')),
    (DONE, __('DONE')),
)

REMODEL = "R"
NEW_BUILT = "N"
PROJECT_TYPE = ((REMODEL, __('REMODEL')),
    (NEW_BUILT, __("NEW BUILT HOUSE")),
)


# get a UUID
def get_a_uuid(*argv):
    if len(argv) == 0:
        r_uuid = str(uuid.uuid4())
        return r_uuid
    elif len(argv) == 1:
        # in python 2.x TODO: need to add case in python 3.x
        if isinstance(argv[0], basestring):
            try:
                model = ContentType.objects.get(model=argv[0])
            except ContentType.DoesNotExist:
                print("Does Not Exist!")
        else:
            try:
                model = ContentType.objects.get_for_model(argv[0])
            except ContentType.DoesNotExist:
                print("Does Not Exist!")
        flag = True
        while flag:
            try:
                r_uuid = str(uuid.uuid4())
                object = model.get_object_for_this_type(uuid=r_uuid)
            except model.model_class().DoesNotExist:
                flag = False
        return r_uuid
    else:
        raise Exception('%d arguments given, which requires 1.' % (len(argv)))
