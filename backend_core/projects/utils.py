import uuid
from django.utils.translation import ugettext_lazy as __

WAITING = "Waiting"
WITHDRAWN = "Withdrawn"
RETURNED = "Returned"
PAYED_TO_HOOME = "Payed to Hoome"
PAYED_TO_CONTRACTOR = "Payed to Contractor"
SUCCESS = "Success"


WAITING_ACTION = "Contractor is waiting for the payment"

PENDING = 'P'
ACCEPTED = 'A'
REJECTED = 'R'
ONGOING = "O"
DONE = "D"

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
