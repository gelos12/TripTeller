from django.shortcuts import render
from rest_framework import viewsets, generics, filters
from . import models
from . import serializers
from django.db.models import Q, Count

#유저 검색 필터링
class UserListFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        flt = {}        
        for param in request.query_params:
            if param == 'user':
                user = models.User.objects.filter(email=request.query_params[param]).first()
                flt['email'] = user.email
            else:
                for fld in view.filter_fields:
                    if param.startswith(fld):
                        flt[param] = request.query_params[param]
        return queryset.filter(**flt)


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

#유저 정보 뷰
class UserListAPIView(generics.ListAPIView):
    #permission_classes = [permissions.IsAuthenticated]  
    model = models.User
    queryset = models.User.objects.all()
    serializer_class = serializers.UserListSerializer
    filter_backends = (UserListFilterBackend,)
    filter_fields =('user',)

#유저 정보 뷰
class UserRankingListAPIView(generics.ListAPIView):
    #permission_classes = [permissions.IsAuthenticated]  
    model = models.User
    queryset = models.User.objects.all()
    serializer_class = serializers.UserRankingListSerializer

    def get_queryset(self):
        queryset = super(UserRankingListAPIView, self).get_queryset()
        queryset = queryset.annotate(review=Count('review_set')).order_by('-review') # TODO
        return queryset