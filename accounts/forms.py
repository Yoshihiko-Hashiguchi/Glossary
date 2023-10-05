from django import forms
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import validate_password
# from .models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class UserRegistForm(forms.ModelForm):
    # username = forms.CharField(label="ユーザー名", widget=forms.TextInput(attrs={'class': 'name-class'}))
    # email = forms.EmailField(label="Eメール", widget=forms.TextInput(attrs={'class': 'email-class'}))
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="パスワード(再入力)", widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean() # clean関数をオーバーライド
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが一致しません。')
    
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user) # パスワードのバリデーション
        user.set_password(self.cleaned_data['password']) # パスワードの暗号化
        # user.set_password(self.cleaned_data.get('password'))
        user.save() # User情報の保存
        return user # 保存したデータを返す

''' # class Metaでmodel=Userにすると、Eメールが重複するエラーでログインできなくなった
class LoginForm(forms.ModelForm):
    email = forms.CharField(label="Eメール", widget=forms.TextInput())
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())

    class Meta:
        model = User
        # fields = ['username', 'password']
        fields = ['email', 'password']
# '''

class LoginForm(forms.Form):
    # username = forms.CharField(label="ユーザー名")
    email = forms.CharField(label="Eメール",) # EmailFieldでもOK
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())


class UserUpdateForm(forms.ModelForm):
    # password = ReadOnlyPasswordHashField() # パスワードを変更しない場合
    username = forms.CharField(label="ユーザー名")
    last_name = forms.CharField(label="姓")
    first_name = forms.CharField(label="名")
    email = forms.EmailField(label="Eメール")
    target_asset_amount = forms.IntegerField(label="目標金額")
    profiel = forms.CharField(label="プロフィール", widget=forms.Textarea())
    # picture = forms.FileField(label="プロフィール画像", required=False)
    
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'target_asset_amount', 'profiel')
        # fields = ('username', 'first_name', 'last_name', 'email', 'target_asset_amount', 'profiel', 'picture')
    
    # def clean_password(self):
    #     return self.initial['password'] # パスワードを変更できないように初期値のパスワードを返す


class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="パスワード(再入力)", widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('password',)
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが一致しません。')
        
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class UserDeleteForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = []