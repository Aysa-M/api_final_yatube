from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Comment, Follow, Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """
    Allowed requests: GET, PUT, PATCH, DELETE. Getting, editing or deleting
    exact post by its id.
    """
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Viewset for CRUD (GET, PUT, PATCH, DELETE) of a requested Comment objects.
    Allowed requests: GET, PUT, PATCH, DELETE. Getting, editing or deleting
    a requested Comment object of a chosen post by its id.
    """
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)
        return post.comments.all()


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """
    Viewset for getting a queryset or retrieve a model instance.
    """
    pass


class GroupViewSet(ListRetrieveViewSet):
    """
    Displays a list of all groups or a current group on the social net.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class ListCreateViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Viewset for getting a queryset or create a model object.
    """
    pass


class FollowViewSet(ListCreateViewSet):
    """
    Viewset for CRUD (GET, CREATE) of requested Follow objects.
    Get a list of all followings or create a new one which are related
    to the request user.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        new_queryset = Follow.objects.filter(user=self.request.user.id)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
