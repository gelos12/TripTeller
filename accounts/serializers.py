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
            return "http://"+self.context['request'].META['HTTP_HOST']+"/static/ubuntu.png"
        return 'error'

    def validate_password(self,pwd):
        return make_password(pwd)