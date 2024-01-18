from rest_framework import serializers

from market_app.models import Advertisement, Review


class AdvertisementSerializer(serializers.ModelSerializer):
    review = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = '__all__'

    def get_review(self, obj):
        if obj.review_set.all():
            review_list = [review.text for review in obj.review_set.all()]
            return review_list
        return 'Nobody wants to comment it!'

    def get_review_count(self, obj):
        return obj.review_set.count()


class MyAdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
