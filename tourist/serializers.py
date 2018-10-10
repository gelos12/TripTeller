from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
from . import Fields
from django.db.models import Avg
class CommentSerializer(serializers.ModelSerializer):
    author = Fields.AuthorField()
    class Meta:
        model = models.Comment
        #보여주기위해서 fields 변수 튜플에 들어가있어야한다.
        fields = ('review','author','content','created_at','updated_at')
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        } 

#후기 사진 생성 시리얼라이저
class ReViewPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReViewPhoto
        fields = ('photo',)

class CommentReViewSerializer(serializers.ModelSerializer):
    photo = ReViewPhotoSerializer(source='reviewphoto_set',many=True,read_only=True)
    comment = CommentSerializer(source='comment_set', many=True, read_only=True)
    content_id = Fields.ContentIdField()
    author = Fields.AuthorField()
    like = serializers.SerializerMethodField()
    class Meta:
        model = models.ReView
        fields = ('pk','content_id', 'author', 'content', 'star_score', 'created_at', 'updated_at', 'like','photo','comment','areacode','sigungucode')
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
    def get_like(self,obj):
        return obj.like_count
    
#후기 생성 시리얼라이저
class ReViewSerializer(serializers.ModelSerializer):
    photo = ReViewPhotoSerializer(source='reviewphoto_set',many=True,read_only=True)
    content_id = Fields.ContentIdField()
    author = Fields.AuthorField()
    like = serializers.SerializerMethodField()

    class Meta:
        model = models.ReView
        fields = ('pk','content_id', 'author', 'content', 'star_score', 'created_at', 'updated_at', 'like','photo','areacode','sigungucode')
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
    def get_like(self,obj):
        return obj.like_count
        
    def create(self, validated_data):
        photo_datas = self.context.get('view').request.FILES
        review = models.ReView.objects.create(content_id=validated_data.get('content_id'),
        author = validated_data.get('author'),
        content = validated_data.get('content'),
        star_score = validated_data.get('star_score'),
        areacode = validated_data.get('areacode'),
        sigungucode = validated_data.get('sigungucode'),
        )
        for photo in photo_datas.getlist('photo'):
            models.ReViewPhoto.objects.create(review=review,photo=photo)

        return review

#관광지 시리얼라이저
#찜 갯수/ 리뷰 갯수 / 총 평점
class TouristSpotSerializer(serializers.ModelSerializer):
    star = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()
    mark = serializers.SerializerMethodField()
    class Meta:
        model = models.TouristSpot
        #보여주기위해서 fields 변수 튜플에 들어가있어야한다.
        fields = ('content_id','star','review','mark')

    def get_star(self, obj):
        a= obj.review_set.aggregate(Avg('star_score'))
        if a['star_score__avg'] == None:
            return 0
        return a['star_score__avg']

    def get_review(self, obj):
        return obj.review_set.count()
    #tourist/?email=이메일 
    def get_mark(self, obj):
        query = self.context.get('request').query_params
        #쿼리가 있다면
        if query:
            user = get_user_model().objects.filter(email=query['email']).first()
            is_mark = obj.mark_set.filter(user=user)
            if not is_mark:
                return False
            else:
                return True
        return False

class SpotMarkSerializer(serializers.ModelSerializer):
    content_id = Fields.ContentIdField()
    user = Fields.AuthorField()
    class Meta:
        model = models.SpotMark
        #보여주기위해서 fields 변수 튜플에 들어가있어야한다.
        fields = ('content_id','user',) 
    

class ReViewLikeSerializer(serializers.ModelSerializer):
    user = Fields.AuthorField()
    class Meta:
        model = models.ReViewLike
        #보여주기위해서 fields 변수 튜플에 들어가있어야한다.
        fields = ('review','user',) 

