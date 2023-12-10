from rest_framework import serializers
from .models import Question, QComment, Tag

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('faculty_and_department', 'content', 'anser', 'tag', 'is_public', 'created_at')

#class FacultySerializer(serializers.ModelSerializer):
#    class Meta:
#        model = 

class QCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QComment
        fields = ('id', 'no', 'question', 'comment', 'pub_fig', 'created_at')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag', 'url_code', 'sort')
