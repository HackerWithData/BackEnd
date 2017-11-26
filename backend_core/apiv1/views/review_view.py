from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.review_serializer import ReviewSerializer
from review.models import Review
from architects.models import Architect


class ReviewDetail(CreateAPIView):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    #
    # def create(self, request, *args, **kwargs):
    #     try:
    #         lic_num = self.request.resolver_match.kwargs['pk']
    #         architect = Architect.objects.get(lic_num=lic_num)
    #     except:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #     return super(ReviewCreateAPIView, self).create(request, *args, **kwargs)