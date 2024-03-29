import datetime

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from .models import (
    BondHistory,
    WorkerCompensationHistory,
    ComplaintOverall,
)


def convert_hscore_to_rank(hscore=None):
    if not hscore:
        return None
    if hscore.score > 89:
        letter_grade = "A+++"
    elif hscore.score > 80:
        letter_grade = "A++"
    elif hscore.score > 75:
        letter_grade = "A+"
    elif hscore.score > 70:
        letter_grade = "A"
    elif hscore.score == 0:
        letter_grade = _("Warning")
    else:
        letter_grade = 'A-'
    return letter_grade


# TODO: need to change in the future
def get_state_full_name(state):
    FullName = "California"
    return FullName


# TODO: need to revise here
def avg_rating(review=None, rt=None):
    if not review or not rt:
        return None
    s = 0
    l = 0
    if review:
        for r in review:
            rate_list = [i.rating_score for i in r.userrating_set.all() if i.rating_type == rt]
            s += sum(rate_list)
            l += len(rate_list)
        try:
            return s * 1.0 / l
        except ZeroDivisionError:
            return 0
    else:
        return 0


def get_bond_history(contractor_id=None):
    if not contractor_id:
        return None
    bond_history = BondHistory.objects.filter(contractor_id=contractor_id).order_by('-bond_effective_date').first()
    return bond_history


def get_wc_history(contractor_id=None):
    if not contractor_id:
        return None
    wc_history = WorkerCompensationHistory.objects.filter(contractor_id=contractor_id).order_by(
        '-insur_effective_date').first()
    return wc_history


def get_complaint(contractor=None):
    if not contractor:
        return None
    try:
        complaint = ComplaintOverall.objects.get(contractor=contractor)
    except ObjectDoesNotExist:
        complaint = ComplaintOverall.objects.create(
            **{
                'contractor': contractor,
                'case': 0,
                'citation': 0,
                'arbitration': 0,
                'complaint': 0,
            }
        )
    return complaint


def get_contractor_lic_length(contractor=None):
    if not contractor:
        return None
    if (contractor.lic_expire_date is not None) and (contractor.lic_expire_date < datetime.date.today()):
        length = int(contractor.lic_expire_date.year - contractor.lic_issue_date.year)
    # test issue, won't happen in prod
    elif (not contractor.lic_expire_date) and (not contractor.lic_issue_date):
        length = 0
    else:
        length = int(datetime.date.today().year - contractor.lic_issue_date.year)
    return length

