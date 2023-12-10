from enum import Flag
from posixpath import basename
from statistics import mode
from wsgiref.simple_server import demo_app
from django.db import models


class ReviewManager(models.Manager):
    # Review操作に関する処理を追加
    pass

class Tag(models.Model):
    """
    質問のタグ
    履修登録・学生生活・一人暮らし・サークル・その他
    """
    tag = models.CharField('カテゴリ名', max_length=20)
    url_code = models.IntegerField('URLコード', null=True, blank=False, unique=True)
    sort = models.IntegerField(verbose_name='ソート', default=0)

    class Meta:
        db_table = 'tag'
        verbose_name = 'カテゴリ'
        verbose_name_plural = 'カテゴリ一覧'

    def __str__(self):
        return self.tag

class Faculty(models.Model):
    """
    学部
    """
    faculty = models.CharField('学部名', max_length=20)
    url_code = models.IntegerField('URLコード', null=True, blank=False, unique=True)

    class Meta:
        db_table = 'faculty'
        verbose_name = '学部'
        verbose_name_plural = '学部一覧'

    def __str__(self):
        return self.faculty

class Department(models.Model):
    """
    学科
    """
    department = models.CharField('学科名', max_length=20)
    url_code = models.IntegerField('URLコード', null=True, blank=False, unique=True)
    faculty = models.ForeignKey(
        Faculty,
        verbose_name='学部',
        null=True,
        blank=False,
        on_delete=models.PROTECT,
    )

    class Meta:
        db_table = 'department'
        verbose_name = '学科'
        verbose_name_plural = '学科一覧'

    def __str__(self):
        return self.department


class Question(models.Model):
    """
    質問それ自体
    """
    faculty = models.ForeignKey(
        Faculty,
        verbose_name='学部',
        null=True,
        blank=False,
        on_delete=models.PROTECT,
    )
    department = models.ForeignKey(
        Department,
        verbose_name='学科',
        null=True,
        blank=False,
        on_delete=models.PROTECT,
    )
    content = models.TextField(
        verbose_name='本文',
        null=False,
        blank=False
    )
    tag = models.ForeignKey(
        Tag,
        verbose_name='カテゴリ',
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    anser = models.TextField(
        verbose_name='回答',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    is_public = models.BooleanField(
        default=False if anser != None else True
    ) # 書き込まれた質問は回答が付くまで公開されない

    class Meta:
        db_table = 'question'
        verbose_name = '質問'
        verbose_name_plural = '質問一覧'

    def __str__(self):
        return self.content


class QComment(models.Model):
    """
    質問とその回答に対するコメント
    """
    id = models.BigAutoField(
        primary_key=True,
    )
    no = models.IntegerField(
        default=0,
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
    )
    comment = models.TextField(
        verbose_name='コメント'
    )
    pub_fig = models.BooleanField(
        default=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = 'qcomment'
        verbose_name = 'コメント'
        verbose_name_plural = 'コメント一覧'

    def __str__(self):
        return '{}-{}'.format(self.question.id, self.no)

class VoteManager(models.Manager):
    def create_vote(self, ip_address, qanda_id):
        vote = self.model(
            ip_address=ip_address,
            q_id = qanda_id
        )
        try:
            vote.save()
        except:
            return False
        return True
    
class Vote(models.Model):
    review = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True,
    )
    ip_address = models.CharField(
        'IPアドレス',
        max_length=50,
    )

    objects = VoteManager()

    def __str__(self):
        return '{}-{}'.format(self.review.topic.title, self.review.no)