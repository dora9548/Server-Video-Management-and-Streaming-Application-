from django.urls import path

from .views import video_list, add_video, edit_video, delete_video,user_login,deatils_video
from django.conf import settings
from django.conf.urls.static import static
from . import views

from .views import VideoListCreateAPIView, VideoRetrieveUpdateDestroyAPIView


urlpatterns = [
 
    path('login/', user_login, name='login'),
    path('signup/', views.signup, name='signup'),

   
    path('list/', video_list, name='video_list'),
    path('add/', add_video, name='add_video'),
    path('edit/<int:video_id>/', edit_video, name='edit_video'),
    path('details/<int:video_id>/', deatils_video, name='deatils_video'),
    path('delete/<int:video_id>/', delete_video, name='delete_video'),
    path('list/stream.html/', views.video_stream, name='video_stream'),
    path('search/', views.search_videos, name='search_videos'),

    path('api/videos/', VideoListCreateAPIView.as_view(), name='video-list-create'),
    path('api/videos/<int:pk>/', VideoRetrieveUpdateDestroyAPIView.as_view(), name='You-can--retrieve-update-destroy-videos'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

