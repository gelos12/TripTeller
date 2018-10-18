from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tourist', views.TouristSpotViewSet, base_name='tourist')
router.register(r'mark', views.MarkViewSet, base_name="dmark")
router.register(r'review', views.ReViewViewSet, base_name='review')

router.register(r'like', views.ReViewLikeViewSet, base_name='review_like')
router.register(r'comment', views.CommentViewSet, base_name='comment')
urlpatterns =[
    path('', include(router.urls)),
    path('main/', views.MainReViewViewSet.as_view(), name="main"),
]
