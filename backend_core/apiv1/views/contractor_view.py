import datetime
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from contractors.utils import convert_hscore_to_rank, get_state_full_name, avg_rating
from hscore.models import Hscore
from photos.models import Photo, BackgroundPhoto
from review.models import Review
from contractors.models import Contractor, BondHistory, WorkerCompensationHistory, ComplaintOverall
from overviews.models import Overview
from ..serializers.contractor_serializer import ContractorSerializer


class ContractorDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, object_id):
        try:
            return Contractor.objects.get(pk=object_id)
        except Contractor.DoesNotExist:
            raise Http404

    def get_background_image(self, model_name, object_id):
        try:
            bgimage = BackgroundPhoto.objects.get(content_type=ContentType.objects.get(model=model_name),
                                                  object_id=object_id)
        except BackgroundPhoto.DoesNotExist:
            bgimage = None
        return bgimage

    def get_overview(self, model_name, object_id):
        try:
            overview = Overview.objects.get(content_type=ContentType.objects.get(model=model_name),
                                            object_id=object_id).overview
        except Overview.DoesNotExist:
            overview = None
        return overview

    def get_bond_history(self, object_id):
        try:
            bond_history = BondHistory.objects.filter(contractor_id=object_id).order_by(
                '-bond_effective_date').first()
        except BondHistory.DoesNotExist:
            bond_history = None
        return bond_history

    def get_bond_history(self, object_id):
        try:
            bond_history = BondHistory.objects.filter(contractor_id=object_id).order_by(
                '-bond_effective_date').first()
        except BondHistory.DoesNotExist:
            bond_history = None
        return bond_history

    def get_worker_compensation_history(self, object_id):
        try:
            worker_compensation_history = WorkerCompensationHistory.objects.filter(
                contractor_id=object_id).order_by('-insur_effective_date').first()
        except WorkerCompensationHistory.DoesNotExist:
            worker_compensation_history = None
        return worker_compensation_history

    def get_review(self, object_id):
        try:
            review = Review.objects.filter(content_type=ContentType.objects.get(model='contractor'),
                                           object_id=object_id, review_status='A')
        except:
            review = None
        return review

    def get_compalint(self, object_id):
        try:
            complaint = ComplaintOverall.objects.get(lic_num=object_id)
        except ComplaintOverall.DoesNotExist:
            class Complaint1:
                def __init__(self):
                    self.case = 0
                    self.citation = 0
                    self.arbitration = 0
                    self.complaint = 0

            complaint = Complaint1
            complaint.case = 0
            complaint.citation = 0
            complaint.arbitration = 0
            complaint.complaint = 0
        return complaint

    def get_project_photos(self, model_name, object_id):
        try:
            project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model=model_name),
                                                  object_id=object_id)
        except Photo.DoesNotExist:
            project_photos = None
        return project_photos

    def calc_length(self, contractor):
        if (contractor.lic_expire_date is not None) and (contractor.lic_expire_date < datetime.date.today()):
            length = int(contractor.lic_expire_date.year - contractor.lic_issue_date.year)
        # test issue, won't happen in prod
        elif (not contractor.lic_expire_date) and (not contractor.lic_issue_date):
            length = 0
        else:
            length = int(datetime.date.today().year - contractor.lic_issue_date.year)
        return length

    def get(self, request, object_id):
        # contractor info
        contractor = self.get_object(object_id)
        # contractor background image
        contractor.bgimage = self.get_background_image('contractor', object_id)
        contractor.bond_history = self.get_bond_history(object_id)
        contractor.worker_compensation_history = self.get_worker_compensation_history(object_id)
        hscore = Hscore.objects.get(contractor_id=object_id)
        letter_grade = convert_hscore_to_rank(hscore)
        full_state_name = get_state_full_name(contractor.state)
        lic_type = contractor.lic_type.split('&')
        review = self.get_review(object_id)
        if review is not None:
            contractor.review = self.get_review(object_id)

        complaint = self.get_compalint(object_id)
        if complaint is not None:
            contractor.complaint = self.get_compalint(object_id)
        contractor.project_photos = self.get_project_photos('contractor', object_id)
        contractor.length = self.calc_length(contractor)

        # if self.get_overview('contractor',contractor_id) is None:
        #     data_source = 'California Contractors State License Board'
        #     overview = _("""{lic_name} is a contractor company located in {csp} . The company holds a license number
        #     according to {data_source}. According to real-time data analysis, this licensed contractor's hoome score
        #     is {score} and is rated as {rank}. The License is verified as active when we checked last time. If you would
        #      like to know {lic_name} more, please contact us and we will share more information and data about this
        #       contractor to you.""").format(lic_name=contractor.lic_name, csp=contractor.csp,
        #                                     data_source=data_source,
        #                                     score=hscore.score, rank=letter_grade, full_state_name=full_state_name)
        # #this part is not finished. Need to consider how send the overview info
        # overview_form = OverviewForm(initial={'overview': overview})


        # rating
        # RATING_STAR_MAX = 10
        # contractor_ratings = Rating.objects.filter(content_type=ContentType.objects.get(model='contractor'),
        #                                            object_id=contractor_id).order_by('ratings_average')
        # ratings = {}
        # ratings['stars'] = range(RATING_STAR_MAX, 0, -1)
        # TODO:NEED TO CHANGE HERE
        # ratings['overall'] = (avg_rating(review, 'Q') + avg_rating(review, 'E') + avg_rating(review, 'L')) / 3
        # try:
        #     ratings['rate'] = [(item.average, round(item.average * 1.0 / RATING_STAR_MAX, 2)) for item in
        #                        contractor_ratings]
        # except:
        #     pass
        #
        # if request.user.is_anonymous():
        #     p_lic_num = None
        # else:
        #     try:
        #         p_lic_num = int(request.user.professional_profiles.first().professional.lic_num)
        #     except:
        #         p_lic_num = None
        #
        # # other situation
        # user_rating_form = UserRatingForm()
        # if request.user.is_authenticated:
        #     review_form = ReviewForm(initial={'first_name': request.user.first_name,
        #                                       'last_name': request.user.last_name,
        #                                       'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})
        # else:
        #     review_form = ReviewForm(initial={
        #         'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})
        serializer = ContractorSerializer(contractor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        contractor = self.get_object(pk)
        serializer = ContractorSerializer(contractor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
