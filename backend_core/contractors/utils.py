from django.utils.translation import ugettext_lazy as _
from .models import (
    BondHistory,
    WorkerCompensationHistory,
    ComplaintOverall,
)
import datetime



def convert_hscore_to_rank(hscore):
    # percentage = round(hscore.rank * 100.0 / hscore.max, 2)
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
def avg_rating(review, rt):
    s = 0
    l = 0
    if review:
        for r in review:
            rate_list = [i.rating_score for i in r.userrating_set.all() if i.rating_type == rt]
            s += sum(rate_list)
            l += len(rate_list)
        return s * 1.0 / l
    else:
        return 0


def get_bh(contractor_id):
    bh = BondHistory.objects.filter(contractor_id=contractor_id).order_by('-bond_effective_date').first()
    return bh


def get_wh(contractor_id):
    wh = WorkerCompensationHistory.objects.filter(contractor_id=contractor_id).order_by(
        '-insur_effective_date').first()
    return wh


def get_complaint(contractor):
    try:
        complaint = ComplaintOverall.objects.get(contractor=contractor)
    except ComplaintOverall.DoesNotExist:
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


def get_contractor_lic_length(contractor):
    if (contractor.lic_expire_date is not None) and (contractor.lic_expire_date < datetime.date.today()):
        length = int(contractor.lic_expire_date.year - contractor.lic_issue_date.year)
    # test issue, won't happen in prod
    elif (not contractor.lic_expire_date) and (not contractor.lic_issue_date):
        length = 0
    else:
        length = int(datetime.date.today().year - contractor.lic_issue_date.year)
    return length

