#django 
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import QueryDict

#rest framework
from rest_framework import viewsets,generics
from rest_framework import views, permissions, status
from rest_framework.response import Response

#module
from django_filters.rest_framework import DjangoFilterBackend
from . import serializers
from . import models
from . import touristFilterBackends
from django_filters.rest_framework import DjangoFilterBackend

#관광지 뷰
class TouristSpotViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated]
    queryset = models.TouristSpot.objects.all()
    serializer_class = serializers.TouristSpotSerializer
    filter_backends = (touristFilterBackends.TouristFilterBackend,)

#관광지 후기 뷰
class ReViewViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated]  
    queryset = models.ReView.objects.all()
    serializer_class = serializers.ReViewSerializer
    filter_backends = (touristFilterBackends.ReViewContentFilterBackend, )
    filter_fields = ('content_id','areacode','sigungucode','author')

    #생성순 정렬
    def get_queryset(self):
        queryset = super(ReViewViewSet, self).get_queryset()
        queryset = queryset.order_by('-created_at') 
        return queryset

#메인 후기 뷰
class MainReViewViewSet(generics.ListAPIView):
    #permission_classes = [permissions.IsAuthenticated]  
    model = models.ReView
    queryset = models.ReView.objects.all()
    serializer_class = serializers.CommentReViewSerializer
    filter_backends = (touristFilterBackends.ReViewContentFilterBackend,)
    
    def get_queryset(self):
        queryset = super(MainReViewViewSet, self).get_queryset()
        queryset = queryset.annotate(like=Count('like_user_set')).order_by('-like') # TODO
        
        return queryset

class MarkViewSet(viewsets.ModelViewSet):
    queryset = models.SpotMark.objects.all()
    serializer_class = serializers.SpotMarkSerializer
    filter_backends = (touristFilterBackends.MarkFilterBackend,)
    filter_fields = ('user')

    #사용자가 보낸 객체 저장 방식 지정
    def perform_create(self, serializer):
        tourist = serializer.validated_data['content_id']
        user = serializer.validated_data['user']

        #시리얼라이저에서 이미 검증된 데이터를 통해 get_or_create를 진행한다.
        tourist_mark, tourist_mark_created = tourist.mark_set.get_or_create(user=user)

        #이미 만들어져 있다면
        if not tourist_mark_created:        
            tourist_mark.delete()
        
        #아니라면 아무런 작업을 하지않는다.
            
class ReViewLikeViewSet(viewsets.ModelViewSet):
    queryset = models.ReViewLike.objects.all()
    serializer_class = serializers.ReViewLikeSerializer

    #사용자가 보낸 객체 저장 방식 지정
    def perform_create(self, serializer):
        review = serializer.validated_data['review']
        user = serializer.validated_data['user']

        #시리얼라이저에서 이미 검증된 데이터를 통해 get_or_create를 진행한다.
        review_like, review_like_created = review.like_set.get_or_create(user=user)

        #이미 만들어져 있다면
        if not review_like_created:        
            review_like.delete()
        
        #아니라면 아무런 작업을 하지않는다.

class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer