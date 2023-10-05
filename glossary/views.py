from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from . import forms
from .models import Terms, Comments
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def term_create(request):
    form = forms.TermCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.instance.update_user = request.user.username
        form.save()
        messages.success(request, '用語を登録しました。')
        return redirect('glossary:term_list')
    return render(request, 'glossary/term_create.html', context={
        'form': form
    })


# def term_list(request, key):
    # if key:
    #     terms = Terms.objects.fetch_part_term(key)
    # else:
    #     terms = Terms.objects.fetch_all_terms()
def term_list(request):
    terms = Terms.objects.fetch_all_terms()
    return render(request, 'glossary/term_list.html', context={
        'terms': terms
    })

'''
def term_detail(request, id):
    term = Terms.objects.filter(pk=id).first()
    return render(request, 'glossary/term_detail.html', context={
        'term': term,
    })
# '''
def term_detail(request, term_id):
    term = get_object_or_404(Terms, id=term_id)
    form = forms.CommentsPostForm(request.POST or None)
    comments = Comments.objects.fetch_by_term_id(term_id)
    if form.is_valid():
        form.instance.term = term
        form.instance.user = request.user
        form.save()
        return redirect('glossary:term_detail', term_id=term_id)
    return render(request, 'glossary/term_detail.html', context={
        'form': form,
        'term': term,
        'comments': comments,
    })


@login_required
def term_update(request, term_id):
    # term = get_object_or_404(term, id=id)
    term = Terms.objects.filter(pk=term_id).first()
    form = forms.TermUpdateForm(request.POST or None, request.FILES or None, instance=term)
    if form.is_valid():
        form.instance.update_user = request.user.username
        form.save()
        messages.success(request, '用語を更新しました。')
        return redirect('glossary:term_detail', term_id=term_id)
    return render(request, 'glossary/term_update.html', context={
        'form': form
    })


@login_required
def term_delete(request, term_id):
    term = Terms.objects.filter(pk=term_id).first()
    form = forms.TermDeleteForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        term.delete()
        messages.success(request, '用語を削除しました。')
        return redirect('glossary:term_list')
    return render(request, 'glossary/term_delete.html', context={
        'form': form,
        'term': term
    })

# ''' # term_detailへ追加
@login_required
def comments_post(request, term_id):
    term = get_object_or_404(Terms, id=term_id)
    form = forms.CommentsPostForm(request.POST or None)
    comments = Comments.objects.fetch_by_term_id(term_id)
    if form.is_valid():
        form.instance.term = term
        form.instance.user = request.user
        form.save()
        return redirect('glossary:term_detail', term_id=term_id)
    return render(request, 'glossary/comments_post.html', context={  
        'form': form,
        'term': term,
        'comments': comments,
    })
# '''

'''
@login_required
def comment_delete(request, term_id):
    comments = Comments.objects.fetch_by_term_id(term_id)
    form = forms.CommentsDeleteForm(request.POST or None)
    if form.is_valid():
        comments.delete()
        messages.success(request, 'コメントを削除しました。')
        return redirect('glossary:term_detail', term_id=term_id)
    return render(request, 'glossary/comments_delete.html', context={
        'form': form,
        'comment': comments
    })
# '''
@login_required
def comment_delete(request, comment_id):
    # comment = Comments.objects.filter(pk=comment_id).first()
    comment = get_object_or_404(Comments, pk=comment_id)
    if comment.user.id != request.user.id:
        raise Http404
    form = forms.CommentsDeleteForm(request.POST or None)
    if form.is_valid():
        comment.delete()
        messages.success(request, 'コメントを削除しました。')
        return redirect('glossary:term_detail', term_id=comment.term.id)
    return render(request, 'glossary/comments_delete.html', context={
        'form': form,
        'comment': comment
    })