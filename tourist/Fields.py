from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model

#원하는 입/출력을 위해 필드 재정의
class ContentIdField(serializers.Field):
    #응답값으로 보여줄 string을 리턴
    def to_representation(self,obj):
        return obj.content_id

    #요청으로 받은 값을 obj로 변경하여 obj를 리턴
    def to_internal_value(self,data):
        content_id = models.TouristSpot.objects.filter(content_id=data).first()
        if content_id is None:
                content_id = models.TouristSpot.objects.create(content_id=data)
        return content_id

class AuthorField(serializers.Field):
    def to_representation(self,obj):
        return obj.nickname

    def to_internal_value(self, data):
        author = get_user_model().objects.filter(email=data).first()
        if author is None:
            raise serializers.ValidationError("없는 계정입니다.")
        return author