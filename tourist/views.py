#django 
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import QueryDict
from django.db.models import Q, Count

#rest framework
from rest_framework import viewsets
from rest_framework import views, permissions, status
from rest_framework.response import Response

#module
from django_filters.rest_framework import DjangoFilterBackend
from . import serializers
from . import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
import functools

#후기 필터링
class ReViewContentFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        flt = {}
        for param in request.query_params:
            if param == 'content_id':
                flt[param] = models.TouristSpot.objects.filter(content_id=request.query_params[param]).first()
            elif param == 'filter':
                if request.query_params[param] == 'True':
                    queryset.order_by('-created_at')
            else:
                for fld in view.filter_fields:
                    if param.startswith(fld):
                        flt[param] = request.query_params[param]
        return queryset.filter(**flt)

#관광지 필터링
class TouristFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        flt = {}
        or_list=[]

        #content_id 를 &로 중복(Overlap)해서 줄경우 어떻게 처리해야할까?
        #content_id 리스트를 만들자.
        #직접 path를 url을 통해서 받아와 작업해준다.
        for ttt in request.get_full_path_info().split('&'):
            if not 'content_id' in ttt: 
                pass
            elif 'api/tourist/' in ttt:
                #or_q |= Q(content_id= ttt.replace('/api/tourist/?content_id=',""))
                or_list.append(ttt.replace('/api/tourist/?content_id=',""))
            elif 'content_id' in ttt:
                #or_q |= Q(content_id=ttt.replace("content_id=",""))
                or_list.append(ttt.replace('content_id=',''))

        #기존 or_q는 예외작업이 불가해서 리스트 방식으로 변경
        #리스트로 content_id를 받아드리고
        #하나하나 확인해서 없다면 생성한다.
        for data in or_list:
            tourist = models.TouristSpot.objects.filter(content_id=data).first()
            if tourist is None:
                models.TouristSpot.objects.create(content_id=data)
        
        #요청한 쿼리셋만 or 하는 문장
        if or_list:
            queryset = queryset.filter(functools.reduce(lambda x, y :x | y, [Q(content_id=item) for item in or_list]))
        
        #순서대로 출력해주기 위해 한땀한땀 순서를 정해준다.
        whens= []
        idx=0
        for qs in queryset:
            idx=0
            for cur in or_list:
                if qs.content_id == int(or_list[idx]):
                    whens.insert(idx, qs)
                idx +=1

        #for param in request.query_params:
            
            # #content_id로 필터 요청한다면
            # if param == 'content_id':
            #     #콤마를 구분하여 여러개의 content_id를 입력받을 수 있다.
            #     for q in request.query_params[param].split(','):
            #         #or 검색 쿼리문을 만들고
            #         or_q |= Q(content_id=q)  
            #     #필터에 적용한다.
            #     queryset = queryset.filter(or_q)
            #그외의 작업
            #else:
            # if param != 'content_id':
            #     if param != 'email':
            #         for fld in view.filter_fields:
            #             if param.startswith(fld):
            #                 flt[param] = request.query_params[param]
        #그외 작업 필터링
        return whens

#관광지 뷰
class TouristSpotViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated]
    queryset = models.TouristSpot.objects.all()
    serializer_class = serializers.TouristSpotSerializer
    filter_backends = (TouristFilterBackend,)

#관광지 후기 뷰
class ReViewViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated]  
    queryset = models.ReView.objects.all()
    serializer_class = serializers.ReViewSerializer
    filter_backends = (ReViewContentFilterBackend, )
    filter_fields = ('content_id','areacode','sigungucode')

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
    filter_backends = (ReViewContentFilterBackend,)
    
    def get_queryset(self):
        queryset = super(MainReViewViewSet, self).get_queryset()
        queryset = queryset.annotate(like=Count('like_user_set')).order_by('-like') # TODO
        
        return queryset

class MarkViewSet(viewsets.ModelViewSet):
    queryset = models.SpotMark.objects.all()
    serializer_class = serializers.SpotMarkSerializer


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