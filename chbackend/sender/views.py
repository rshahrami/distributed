from rest_framework import viewsets
from .models import Province, Channel, Post
from .serializers import ProvinceSerializer, ChannelSerializer, PostSerializer

class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        # محدود کردن دسترسی بر اساس کاربر
        if not self.request.user.is_superuser:
            return Post.objects.filter(created_by=self.request.user)
        return Post.objects.all()