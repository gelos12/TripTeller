from rest_framework import filters
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
import functools
from . import models

#찜 필터링
class MarkFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        flt = {}
        for param in request.query_params:
            if param == 'filter':
                if request.query_params[param] == 'True':
                    queryset.order_by('-created_at')
            else:
                for fld in view.filter_fields:
                    if param == 'user':
                        user = get_user_model().objects.filter(email=request.query_params[param]).first()
                        flt[param] = user
                    elif param.startswith(fld):
                        flt[param] = request.query_params[param]
        return queryset.filter(**flt).order_by('-created_at')

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
            elif param =='author':
                user = get_user_model().objects.filter(email=request.query_params[param]).first()
                flt[param] = user
            else:
                for fld in view.filter_fields:    
                    if param.startswith(fld):
                        flt[param] = request.query_params[param]
        if request.query_params.get('areacode') or request.query_params.get('sigungucode'):
            return queryset.filter(**flt).annotate(like=Count('like_user_set')).order_by('-like')
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
        for item in or_list:
            for qs in queryset:
                if int(item) == qs.content_id:
                    whens.append(qs)

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