
from django.shortcuts import render, redirect, get_object_or_404
from .models import Video
import os
from django.http import StreamingHttpResponse
import cv2
import threading
from django.contrib.auth import authenticate, login


from .forms import SignUpForm
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import VideoSerializer
from .forms import VideoForm,LoginForm



##### restapi ###############


class VideoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class VideoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]




##### video stream ######



class VideoStream(threading.Thread):
    def __init__(self, video_file):
        super(VideoStream, self).__init__()
        self.video_file = video_file

    def generate_frames(self):
        cap = cv2.VideoCapture(self.video_file)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            ret, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    def run(self):
        self.frames_iterator = self.generate_frames()

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.frames_iterator)

def video_stream(request):
    if request.method == 'GET':
        video_id = request.GET.get('video_id')
        if video_id:
            video = Video.objects.get(id=video_id)
            video_streamer = VideoStream(video.video_file.path)
            video_streamer.start()
            return StreamingHttpResponse(video_streamer, content_type='multipart/x-mixed-replace;boundary=frame')
    return render(request, 'stream.html')









##### signup and login ##########


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('video_list')  
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('video_list')  
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})







##### main video crud ###########

def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})

def add_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST,request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            form.save()
            video_dir = 'C:/Users/bibhuprasad/New folder/spritleprj/Videos/' 
            for filename in os.listdir(video_dir):
                if filename.endswith('.mp4'): 
                    name = os.path.splitext(filename)[0]
                    path = os.path.join(video_dir, filename)
                    Video.objects.create(name=name, path=path)
            
            return redirect('video_list')
    else:
        form = VideoForm()
    return render(request, 'video_form.html', {'form': form})

def edit_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('video_list')
    else:
        form = VideoForm(instance=video)
    return render(request, 'video_form.html', {'form': form})

def deatils_video(request, video_id):  
    if request.method == 'GET':
        video = get_object_or_404(Video, pk=video_id)
        print(video.name, video.video_file,video_id)
        #n=video.name, p=video.video_file , i=video_id
        context = {
       'video': video,
        'video_id': video_id,
        }
        

        return render(request, 'video_detail.html', context)
   

    

def delete_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if request.method == 'POST':
        video.delete()
        return redirect('video_list')
    return render(request, 'video_confirm_delete.html', {'video': video})

from django.shortcuts import render
from .models import Video

def search_videos(request):
    query = request.GET.get('query')
    videos = Video.objects.all()
    if query:
        videos = videos.filter(name__icontains=query)
    return render(request, 'video_list.html', {'videos': videos})



