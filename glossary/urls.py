from django.urls import path
from . import views

app_name = 'glossary'

urlpatterns = [
    path('term_create', views.term_create, name='term_create'),
    path('term_list', views.term_list, name='term_list'),
    path('term_detail/<int:term_id>', views.term_detail, name='term_detail'),
    path('term_update/<int:term_id>', views.term_update, name='term_update'),
    path('term_delete/<int:term_id>', views.term_delete, name='term_delete'),
    path('comments_post/<int:term_id>', views.comments_post, name='comments_post'),
    path('comment_delete/<int:comment_id>', views.comment_delete, name='comment_delete'),
]