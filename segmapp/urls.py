from django.urls import path
from segmapp import views
app_name='app'
urlpatterns = [
path('create/',views.CreatePost.as_view(),name='create'),
path('postlist/<pk>',views.ListPosts.as_view(),name='posts'),
path('posts/edit/<pk>',views.EditPosts.as_view(),name='edit'),
path('posts/<pk>',views.DetailPosts.as_view(),name='detail'),
path('posts/comment/<slug>',views.comment,name='comment'),
path('posts/comment/delete/<pk>',views.DeleteComment.as_view(),name='delcom'),
path('<pk>',views.follow,name='follow'),
path('following/<pk>',views.Followinglist.as_view(),name='following'),
path('request/<pk>',views.RequestDetail.as_view(),name='request'),
path('accept/<pk>',views.accept,name='accept'),
path('reject/<pk>',views.reject,name='reject'),
path('posts/delete/<pk>',views.PostsDelete.as_view(),name='delete')
]
