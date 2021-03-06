from django.utils.translation import gettext as _
from django.db import models
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField
from django.core.exceptions import ValidationError


class Category(models.Model):
    display_name = models.CharField(max_length=50, unique=True)
    name = models.SlugField(max_length=50, blank=True, unique=True)

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        self.name = slugify(self.display_name)

        return super(Category, self).save(*args, **kwargs)


class Quiz(models.Model):
    SECTION = (
        ('knowledge_quiz', 'Knowledge Quiz'),
        ('universal_quiz', 'Universal Quiz'),
        ('psychology_quiz', 'Psychology Quiz'),
        ('preferential_quiz', 'Preferential Quiz'),
    )

    DEFAULT_IMAGE = 'https://cdn.pixabay.com/photo/2017/01/24/00/21/question-2004314_960_720.jpg'

    DEFAULT_DESCRIPTION = _('Welcome to my quiz!')

    author = models.ForeignKey(
        'accounts.Account', on_delete=models.CASCADE, related_name='quizzes')
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(default=DEFAULT_DESCRIPTION)
    section = models.CharField(max_length=17, choices=SECTION)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, default=1, related_name='quizzes')
    one_page_questions = models.BooleanField(default=False)
    image_url = models.URLField(default=DEFAULT_IMAGE)
    answers_data = models.JSONField(default=list, blank=True)
    solved_times = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    random_question_order = models.BooleanField(default=True)
    password = models.CharField(max_length=20, blank=True)
    ask_name = models.BooleanField(default=True)
    ask_email = models.BooleanField(default=False)
    ask_gender = models.BooleanField(default=False)
    ask_opinion = models.BooleanField(default=True)
    slug = AutoSlugField(populate_from='title',
                         unique_with=['author'], max_length=120)

    def __str__(self):
        return self.title


class QuizPunctation(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='punctations')
    result = models.CharField(max_length=100)
    description = models.TextField()
    slug = AutoSlugField(populate_from='result',
                         unique_with=['quiz'], max_length=120)

    # Universal and knowledge quiz
    from_score = models.PositiveIntegerField()
    to_score = models.PositiveIntegerField()

    def __str__(self):
        return str(self.quiz)


class QuizFeedback(models.Model):
    GENDER = (
        ('man', 'Man'),
        ('woman', 'Woman'),
    )

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=25, blank=True)
    email = models.EmailField(max_length=80, blank=True)
    gender = models.CharField(max_length=5, choices=GENDER, blank=True)
    opinion = models.TextField(blank=True)
    score = models.PositiveIntegerField()

    def __str__(self):
        return str(self.quiz)


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=100)
    image_url = models.URLField(blank=True)
    summery = models.TextField(blank=True)
    slug = AutoSlugField(populate_from='question',
                         unique_with=['quiz'], max_length=120)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['id']


class PsychologyResults(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    result = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = AutoSlugField(populate_from='result',
                         unique_with=['quiz'], max_length=120)

    def __str__(self):
        return self.result


class Answer(models.Model):
    POINTS = (
        ('0', 0),
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
        ('6', 6),
        ('7', 7),
        ('8', 8),
        ('9', 9),
        ('10', 10),
    )

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=100)
    image_url = models.URLField(blank=True)
    slug = AutoSlugField(populate_from='answer', unique_with=[
                         'question'], max_length=120)

    # Knowledge
    is_correct = models.BooleanField(default=False)

    # Universal
    points = models.CharField(max_length=2, choices=POINTS, default=POINTS[0][0])

    # Psychology
    results = models.ManyToManyField(PsychologyResults, blank=True, related_name='answers')

    # Preferentail
    answered_times = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.answer

    class Meta:
        ordering = ['id']
