from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.response import Response

from quizziz.utils import valid_url_extension

from quizzes.models import (
    Quiz,
    Question,
    Category,
    Section,
    PsychologyAnswer,
    PreferentialAnswer,
    PsychologyResults,
    UniversalAnswer,
    KnowledgeAnswer
)


class ImageValidatorSerailizer(serializers.Serializer):
    image_url = serializers.CharField(allow_blank=True)
    success = serializers.BooleanField(default=False, read_only=True)

    def validate(self, data):
        image_url = data.get('image_url')
        data['success'] = False

        if not(image_url.strip()):
            data['success'] = True
            data['image_url'] = Quiz.DEFAULT_IMAGE
        elif valid_url_extension(data['image_url']):
            data['success'] = True
        else:
            data['image_url'] = Quiz.DEFAULT_IMAGE

        return data

    class Meta:
        fields = ('image_url',)
        read_only_fields = ('success',)


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('name', 'display_name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('name', 'display_name')


# class PsychologyResultsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PsychologyResults
#         fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(allow_blank=True)

    def validate_image_url(self, value):
        if not(valid_url_extension(value)):
            return ''

        return value

    class Meta:
        model = Question
        fields = (
            'question',
            'image_url',
            'summery',
            'slug',
        )
        read_only_fields = ('slug',)


class QuizSerializer(serializers.Serializer):
    pub_date = serializers.SerializerMethodField('get_pub_date')
    image_url = serializers.CharField(allow_blank=True)
    section = serializers.CharField(max_length=50)
    category = serializers.CharField(max_length=50)

    def get_pub_date(self, obj):
        return f'{obj.pub_date.day}-{obj.pub_date.month}-{obj.pub_date.year}'

    def validate_section(self, value):
        return Section.objects.get(
            name=value)

    def validate_category(self, value):
        return Category.objects.get(
            name=value)

    def validate_image_url(self, value):
        if not(value.strip()) or not(valid_url_extension(value)):
            return Quiz.DEFAULT_IMAGE

        return value

    def to_representation(self, instance):
        self.fields['section'] = SectionSerializer(read_only=True)
        self.fields['category'] = CategorySerializer(read_only=True)

        return super(QuizSerializer, self).to_representation(instance)


class QuizListSerializer(QuizSerializer, serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_slug = serializers.ReadOnlyField(source='author.slug')

    # def create(self, validated_data):
    #     validated_data['section'] = Section.objects.get(
    #         name=validated_data['section'])

    #     validated_data['category'] = Category.objects.get(
    #         name=validated_data['category'])

    #     return super(self.__class__, self).create(validated_data)

    class Meta:
        model = Quiz
        fields = (
            'pub_date',
            'image_url',
            'section',
            'category',
            'title',
            'description',
            'solved_times',
            'slug',
            'author',
            'author_slug',
            'section',
            'category',
        )
        read_only_fields = ('slug', 'solved_times',)


class QuizDetailSerializer(QuizSerializer, serializers.ModelSerializer):
    questions = serializers.SerializerMethodField('get_questions')
    author = serializers.SerializerMethodField('get_author')

    def get_author(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('account', args=[obj.author.slug]))

    def get_questions(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('quiz-questions', args=[obj.author.slug, obj.slug]))

    class Meta:
        model = Quiz
        exclude = (
            'id',
            'is_published',
            'solved_times',
        )
        read_only_fields = ('questions', 'author',)