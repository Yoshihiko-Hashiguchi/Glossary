from django.shortcuts import render, redirect
from . import forms
from .models import User
import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse

# Create your views here.
def home(request):
    now = datetime.datetime.now()
    return render(request, 'accounts/home.html', context={'now': now,}) # 変数nowを'now'としてhtmlへ渡す


def user_regist(request):
    # form = forms.UserRegistForm()
    # if request.method == 'POST': # Formで送られたデータを取り出す
    #     form = forms.UserRegistForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    form = forms.UserRegistForm(request.POST or None) # forms.UserRegistForm(None)の場合はreturnを実行
    if form.is_valid(): # バリデーション(フィールドが正しいかチェック)
        try:
            form.save() # UserRegistFormのsave関数を実行
            messages.success(request, 'ユーザー登録できました。')
            return redirect('accounts:user_login') # saveがうまくいったらログイン画面に遷移
        except ValidationError as e:
            form.add_error('password', e)
    return render(request, 'accounts/user_regist.html', context={'form': form})


def user_login(request):
    form = forms.LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email') # バリデーションされたデータからemailの要素を取り出す
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password) # emailとpasswordが登録されているものであればTrue
        if user:
            login(request, user)
            messages.success(request, 'ログインしました。')
            return redirect('accounts:home')
        else:
            messages.warning(request, 'Eメールかパスワードが間違っています。')
    return render(request, 'accounts/user_login.html', context={'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'ログアウトしました。')
    return redirect('accounts:home')


@login_required
def user(request, id):
    user = User.objects.filter(pk=id).first()
    return render(request, 'accounts/user.html', context={'user': user})
    # return render(request, 'accounts/user.html')


@login_required
def user_update(request):
    form = forms.UserUpdateForm(request.POST or None, instance=request.user)
    # form = forms.UserUpdateForm(request.POST, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'ユーザー情報を更新しました。')
        # url = reverse('accounts:user', kwargs={'id': request.user.id})
        return redirect(reverse('accounts:user', kwargs={'id': request.user.id}))
    return render(request, 'accounts/user_update.html', context={
        'form': form
    })


@login_required
def password_change(request):
    form = forms.PasswordChangeForm(request.POST or None, instance=request.user)
    if form.is_valid():
        try:
            form.save()
            messages.success(request, 'パスワードを更新しました。')
            update_session_auth_hash(request, request.user)
            return redirect('accounts:user', id=request.user.id)
        except ValidationError as e:
            form.add_error('password', e)
    return render(request, 'accounts/password_change.html', context={
        'form': form
    })


@login_required
def user_delete(request, id):
    user = User.objects.filter(pk=id).first()
    form = forms.UserDeleteForm(request.POST or None)
    if form.is_valid():
        user.delete()
        messages.success(request, 'ユーザーを削除しました。')
        return redirect('accounts:home')
    return render(request, 'accounts/user_delete.html', context={
        'form': form,
        'user': user
    })


def is_staff_check(request):
    if request.user.is_authenticated: # ログインしていれば
        if request.user.is_staff == True: # ユーザーに管理者権限があれば
            return redirect('admin:index')
        else:
            return HttpResponse(
                '<h3>🚨権限がありません🚨</h3>'
                '<h4>権限希望者はサイト作成者へお問合せを！</h4>'
                '<h5>戻るボタンを押してください。</h5>'
            )
    else:
        return redirect('admin:login')