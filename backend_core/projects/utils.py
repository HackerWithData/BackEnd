import uuid
from django.utils.translation import ugettext_lazy as __

WAITING = "W"
PAYED_TO_HOOME = "PTH"
PAYED_TO_PROFESSIONAL = "PTP"

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
    (PAYED_TO_HOOME, __("Payed to Hoome")),
    (PAYED_TO_PROFESSIONAL, __("Payed to Professional")),
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
NEWBUILT = "N"
PROJECT_TYPE = (
    ("", 'N/A'),
    (REMODEL, __('REMODEL')),
    (NEWBUILT, __("NEW BUILT HOUSE")),
)


# get a UUID
def get_a_uuid():
    r_uuid = str(uuid.uuid4())
    return r_uuid
