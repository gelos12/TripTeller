from rest_framework import serializers
from . import models
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = models.User
        fields = ('email','nickname','password','photo','image')
        read_only = ('image',)
        extra_kwargs ={
            'password' : {'write_only':True},
            'photo' :  {'write_only':True},
        }

    def get_image(self, obj):
        if bool(obj.photo) == True:
            return self.context['request'].build_absolute_uri(obj.photo.url)
        else:
            return "http://"+self.context['request'].META['HTTP_HOST']+"/static/user.jpgg"
        return 'error'

    def validate_password(self,pwd):
        return make_password(pwd)

class UserListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    review_cnt = serializers.SerializerMethodField()
    mark_cnt = serializers.SerializerMethodField()
    class Meta:
        model = models.User
        fields = ('image','review_cnt','mark_cnt','nickname')
    
    def get_review_cnt(self, obj):
        return obj.review_set.count()
    #tourist/?email=이메일 

    def get_mark_cnt(self,obj):
        return obj.spotmark_set.count()

    def get_image(self, obj):
        if bool(obj.photo) == True:
            return self.context['request'].build_absolute_uri(obj.photo.url)
        else:
            return "http://"+self.context['request'].META['HTTP_HOST']+"/static/user.jpg"
        return 'error' 

class UserRankingListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    ranking = serializers.SerializerMethodField()
    count = 0

    class Meta:
        model = models.User
        fields = ('ranking','nickname','image','nickname')
        
    def get_review_cnt(self, obj):
        return obj.review_set.count()
    #tourist/?email=이메일 

    def get_ranking(self,obj):
        self.count+=1
        print(self.count)
        return str(self.count)

    def get_image(self, obj):
        if bool(obj.photo) == True:
            return self.context['request'].build_absolute_uri(obj.photo.url)
        else:
            return "http://"+self.context['request'].META['HTTP_HOST']+"/static/user.jpg"
        return 'error' 