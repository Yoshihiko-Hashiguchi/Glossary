from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin # この行はコメントアウト①を使う時にコメントアウトする

# Create your models here.
''' コメントアウト①
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Eメールを入力してください')
        user = self.model(
            username=username, # Userクラスのusernameを流用
            email=email # Userクラスのemailを流用
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None):
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
# '''

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name="ユーザー名", max_length=150)
    email = models.EmailField(verbose_name="Eメール", max_length=255, unique=True)
    is_staff = models.BooleanField(verbose_name="管理者権限", default=False) # 管理画面にログインできるかどうか
    is_active = models.BooleanField(verbose_name="アクティブ", default=True) # ユーザーがアクティブかどうか
    first_name = models.CharField(verbose_name="名", max_length=150, blank=True)
    last_name = models.CharField(verbose_name="姓", max_length=150, blank=True)
    target_asset_amount = models.IntegerField(verbose_name="目標金額", blank=True, default=1000000)
    profiel = models.TextField(verbose_name="プロフィール", blank=True)
    # picture = models.FileField(verbose_name="プロフィール画像", blank=True)
    # password = models.CharField(verbose_name="パスワード", max_length=50) # デフォルトで含まれるため定義不要
    # create_at = models.DateTimeField(verbose_name="作成日時", default=timezone.datetime.now)
    # update_at = models.DateTimeField(verbose_name="更新日時", default=timezone.datetime.now)
    objects = UserManager()
    
    USERNAME_FIELD = 'email' # テーブルのレコードを一意に識別するものを指定する
    REQUIRED_FIELDS = ['username'] # スーパーユーザー作成時に入力するものを指定する

    # 以下、管理画面の設定
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name="ユーザー"
        verbose_name_plural="ユーザー"
        db_table = 'User'
        ordering = ['username']