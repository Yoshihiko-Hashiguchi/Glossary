from django.db import models
from django.utils import timezone

# Create your models here.
class TermsManager(models.Manager):
    
    # 用語の一覧を、昇順で並び替えて取り出す
    def fetch_all_terms(self):
        return self.order_by('term').all()
    
    # 検索に引っかかった用語のみを取り出す
    def fetch_part_term(self, args):
        return self.filter(args).all()


class Terms(models.Model):
    
    term = models.CharField(verbose_name="用語", max_length=50, unique=True)
    explanation = models.TextField(verbose_name="説明")
    picture = models.FileField(verbose_name="画像", upload_to='picture/', blank=True)
    update_user = models.CharField(verbose_name="最終更新者", max_length=50, null=True, default=None)
    update_at = models.DateTimeField(verbose_name="更新日時", default=timezone.datetime.now)
    objects = TermsManager()
    
    def __str__(self): # 管理画面での表示方法
        return self.term # 用語名で表示
    
    class Meta:
        verbose_name="用語"
        verbose_name_plural="用語"
        db_table = 'terms'


class CommentsManager(models.Manager):
    def fetch_by_term_id(self, term_id):
        return self.filter(term_id=term_id).order_by('id').all()


class Comments(models.Model):
    comment = models.CharField(verbose_name="コメント", max_length=1000)
    term = models.ForeignKey(
        'Terms', verbose_name="用語", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'accounts.User', verbose_name="ユーザー", null=True, on_delete=models.SET_NULL
    )
    objects = CommentsManager()
    
    def __str__(self):
        return self.comment
    
    class Meta:
        verbose_name="コメント"
        verbose_name_plural="コメント"
        db_table = 'comments'


class ReplysManager(models.Manager):
    def fetch_by_comment_id(self, comment_id):
        return self.filter(comment_id=comment_id).order_by('id').all()


class Replys(models.Model):
    reply = models.CharField(verbose_name="返信", max_length=1000)
    comment = models.ForeignKey(
        'Comments', verbose_name="コメント", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'accounts.User', verbose_name="ユーザー", null=True, on_delete=models.SET_NULL
    )
    objects = ReplysManager()
    
    def __str__(self):
        return self.reply
    
    class Meta:
        verbose_name="返信"
        verbose_name_plural="返信"
        db_table = 'replys'