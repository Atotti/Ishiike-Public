from enum import Flag
from posixpath import basename
from statistics import mode
from wsgiref.simple_server import demo_app
from django.db import models

"""
    参考 : https://django.kurodigi.com/create-models/

    授業名
    担当教官
    前期後期
    曜日
    時限
"""

class ReviewManager(models.Manager):
    # Review操作に関する処理を追加
    pass


class Semester(models.Model):
    """
    授業の開講期間
    前期か、後期か、集中講義かなど
    """
    semester = models.CharField('開講', max_length=20)
    url_code = models.IntegerField('URLコード', null=True, blank=False, unique=True)
    sort = models.IntegerField(verbose_name='ソート', default=0)

    class Meta:
        db_table = 'semester'
        verbose_name = '開講'
        verbose_name_plural = '開講一覧'

    def __str__(self):
        return self.semester


class Day(models.Model):
    """
    授業が行われている曜日
    集中講義等はその他に
    """
    day = models.CharField('曜日', max_length=10)
    url_code = models.IntegerField('URLコード', null=True, blank=False, unique=True)
    sort = models.IntegerField(verbose_name='ソート', default=0)

    class Meta:
        db_table = 'day'
        verbose_name = '曜日'
        verbose_name_plural = '曜日一覧'

    def __str__(self):
        return self.day


class Period(models.Model):
    """
    何時限目か
    """
    period = models.CharField('時限', max_length=10)
    url_code = models.IntegerField('URLコード', null=True, blank=False, unique=True)
    sort = models.IntegerField(verbose_name='ソート', default=0)

    class Meta:
        db_table = 'period'
        verbose_name = '時限'
        verbose_name_plural = '時限一覧'

    def __str__(self):
        return self.period
"""    
class Attendance(models.Model):

    attendance = models.CharField('出席', max_length=10)
    url_code = models.IntegerField('URLコード', null=True, blank=False, unique=True)
    sort = models.IntegerField(verbose_name='ソート', default=0)

    class Meta:
        db_table = 'attendance'
        verbose_name = '出席'
        verbose_name_plural = '出席一覧'

    def __str__(self):
        return self.attendance
"""


class Review(models.Model):
    """
    クチコミそれ自体
    """
    title = models.CharField(
        "授業名",
        null=False,
        blank=False,
        max_length=30
    )
    semester = models.ForeignKey(
        Semester,
        verbose_name='開講',
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    day = models.ForeignKey(
        Day,
        verbose_name='曜日',
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    period = models.ForeignKey( #この辺りのフィールドはシラバスデータと連携させて自動入力にしたい
        Period,
        verbose_name='時限',
        null=False,
        blank=False,
        max_length=5,
        on_delete=models.PROTECT
    )
    """
    attendance = models.ForeignKey(
        Attendance,
        verbose_name='出席の有無',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    """
    content = models.TextField(
        verbose_name='本文',
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    is_public = models.BooleanField(
        default=True
    ) # 書き込まれたクチコミはデフォルトでは公開されない -> デフォルトで公開されるように変更

    class Meta:
        db_table = 'review'
        verbose_name = 'クチコミ'
        verbose_name_plural = 'クチコミ一覧'

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    クチコミに対するコメント
    """
    id = models.BigAutoField(
        primary_key=True,
    )
    no = models.IntegerField(
        default=0,
    )
    review = models.ForeignKey(
        Review,
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
        db_table = 'comment'
        verbose_name = 'コメント'
        verbose_name_plural = 'コメント一覧'

    def __str__(self):
        return '{}-{}'.format(self.review.id, self.no)

class VoteManager(models.Manager):
    def create_vote(self, ip_address, review_id):
        vote = self.model(
            ip_address=ip_address,
            review_id = review_id
        )
        try:
            vote.save()
        except:
            return False
        return True
    
class Vote(models.Model):
    review = models.ForeignKey(
        Review,
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