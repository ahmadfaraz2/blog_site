from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path('', views.PostListView.as_view(), name='page_list'),
    #path('', views.post_list, name="post_list"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name="post_detail"),
    #path('<int:id>/', views.post_detail, name="post_detail"),
    path('<int:post_id>/share/', views.post_share, name="post_share"),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]



# ------------------------->>>>New Concept<<<<-------------------------------
# Ap ka "url path route" k "parameters"(<int:id>, <int:month>, <slug:post>) important hain jo ap "view" 
# mai pass karty hain. [post_share(request, post_id)].

# Ap "url path route" mai koi b tartib dy skty hain. Bus "parameters" k name wo hi hona chai jo "view" 
# function main ho.