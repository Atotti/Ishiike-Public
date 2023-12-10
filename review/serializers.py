from rest_framework import serializers
from .models import Review, Comment, Semester, Day, Period

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('title', 'semester', 'day', 'period', 'content', 'is_public', 'created_at')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'no', 'review', 'comment', 'pub_fig', 'created_at')

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ('semester', 'url_code', 'sort')

class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ('day', 'url_code', 'sort')

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ('period', 'url_code', 'sort')