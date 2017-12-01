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