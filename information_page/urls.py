from django.urls import path, include

from information_page import views

app_name = 'informations'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('about/', views.AboutPageView.as_view(), name='about'),
]


# Articles urls
articles_url = [
    path('article/', include([
         path('create/',
              views.CreateArticle.as_view(),
              name='article-create'),
         path('<slug:slug>/', include([
              path('',
                   views.ArticleDetails.as_view(),
                   name='article-details'),
              path('update/',
                   views.UpdateArticle.as_view(),
                   name='article-update'),
              path('remove/',
                   views.DeleteArticle.as_view(),
                   name='article-delete'),
              path('publish/',
                   views.publish,
                   name='article-publish')
              ])),
         ])),
    path('articles/', include([
         path('',
              views.AllArticles.as_view(),
              name='all-articles',
              kwargs={'page': 1}),
         path('page/<int:page>/',
              views.AllArticles.as_view(),
              name='all-articles'),
         path('user/<str:username>/', include([
              path('page/<int:page>/',
                   views.AuthorArticles.as_view(),
                   name='author-articles'),
              path('',
                   views.AuthorArticles.as_view(),
                   name='author-articles',
                   kwargs={'page': 1}),
              ])),
         path('drafts/', include([
              path('page/<int:page>/',
                   views.ArticlesInDraft.as_view(),
                   name='article-drafts'),
              path('',
                   views.ArticlesInDraft.as_view(),
                   name='article-drafts',
                   kwargs={'page': 1}),
              ])),
         path('category/<str:category>/', include([
              path('page/<int:page>/',
                   views.ArticlesByCategory.as_view(),
                   name='article-list'),
              path('',
                   views.ArticlesByCategory.as_view(),
                   name='article-list',
                   kwargs={'page': 1}),

              ]))
         ]))
]

urlpatterns.extend(articles_url)


# Genres urls
genres_url = [
    path('informations/genres/', include([
         path('',
              views.GenresList.as_view(),
              name='genre-list',
              kwargs={'page': 1}),
         path('<int:page>/',
              views.GenresList.as_view(),
              name='genre-list'),
         path('create/',
              views.CreateGenre.as_view(),
              name='genre-create'),
         path('<slug:slug>/', include([
              path('details/',
                   views.GenreDetails.as_view(),
                   name='genre-details'),
              path('remove/',
                   views.DeleteGenre.as_view(),
                   name='genre-remove')
              ]))
         ]))
]


urlpatterns.extend(genres_url)


# Comments urls
comments_urls = [
    path('comments/', include([
         path('<str:username>/', include([
              path('page/<int:page>/',
                   views.Comments.as_view(),
                   name='user-comments'),
              path('',
                   views.Comments.as_view(),
                   name='user-comments',
                   kwargs={'page': 1}),
              ])),
         path('create/<slug:slug>/',
              views.create_comment,
              name='comment-create'),
         path('<int:pk>/', include([
              path('remove/',
                   views.DeleteComment.as_view(),
                   name='comment-remove'),
              path('update/',
                   views.UpdateComment.as_view(),
                   name='comment-update')
              ]))
         ]))
]

urlpatterns.extend(comments_urls)


# Notes url
notes_urls = [
    path('notes/', include([
         path('create/<slug:slug>',
              views.create_note,
              name='create-note'),
         path('<int:pk>/', include([
              path('remove/',
                   views.DeleteNote.as_view(),
                   name='note-remove'),
              path('update/',
                   views.UpdateNote.as_view(),
                   name='note-update')
              ])),
         path('user/<str:username>/', include([
              path('page/<int:page>/',
                   views.Notes.as_view(),
                   name='user-notes'),
              path('',
                   views.Notes.as_view(),
                   name='user-notes',
                   kwargs={'page': 1}),
              ]))
         ]))
]

urlpatterns.extend(notes_urls)
