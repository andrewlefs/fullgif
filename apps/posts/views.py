from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .serializers import PostSerializer

from apps.posts.models import Post

class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.order_by('-created_date')
