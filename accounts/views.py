from django.shortcuts import render
from rest_framework import viewsets, generics, filters
from . import models
from . import serializers

#유저 검색 필터링
class UserListFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        flt = {}
        for param in request.query_params:
            for fld in view.filter_fields:
                if param == 'email':
                    user = models.User.objects.filter(email=request.query_params[param]).first()
                    flt[param] = user
                elif param.startswith(fld):
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
    filter_fields =('email',)