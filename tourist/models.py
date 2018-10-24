from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class TouristSpot(models.Model):
    content_id = models.IntegerField(unique=True)
    mark_user_set = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name="ts_mark_user_set",
        through='SpotMark'
    )

    def __str__(self):
        return str(self.content_id)

class SpotMark(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    content_id = models.ForeignKey(
        TouristSpot,
        on_delete=models.CASCADE,
        related_name='mark_set'
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#후기작성
class ReView(models.Model):
    #관광지id, 후기, 후기사진, 별점
    content_id = models.ForeignKey(
        TouristSpot,
        verbose_name='관광지',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    content = models.TextField(
        '후기',
    )

    star_score = models.FloatField(
        '별점',
        default=5.0,        
    )

    like_user_set = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name='rv_like_user_set',
        through='ReViewLike'
        )
    areacode = models.IntegerField()
    sigungucode = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def like_count(self):
        return self.like_user_set.count()

#좋아요
class ReViewLike(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    review = models.ForeignKey(
        ReView,
        on_delete=models.CASCADE,
        related_name='like_set',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ReViewPhoto(models.Model):
    review = models.ForeignKey(
        ReView,
        verbose_name='후기',
        on_delete=models.CASCADE,
    )

    photo = models.ImageField(
        '후기 사진',
        upload_to = 'review/%Y/%m/%d',
        blank=False,     
    )

class Comment(models.Model):
    review = models.ForeignKey(
        ReView,
        verbose_name='후기',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    content = models.TextField('댓글',)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    