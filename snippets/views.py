from snippets.models import Snippet
from rest_framework import generics
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer, SnippetSerializer, FriendSerializer
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly, IsOwnerOrFriend
from django.contrib.auth.hashers import make_password
import logging


class SnippetList(generics.ListCreateAPIView):
    permission_classes = (IsOwnerOrFriend,)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        snippet_list = Snippet.objects.all()
        logger = logging.getLogger(__name__)
        logger.debug(self.request.user.id)
        logger.debug(self.request.user.username)
        logger.debug(self.request.user.password)
        logger.debug(self.request.user.friends)
        logger.debug(self.request.user.snippets)
        temp = User.objects.get(id = self.request.user.id)
        logger.debug(temp.friends)
        self_user = UserSerializer(temp)
        logger.debug(self_user.friends)
        logger.debug(type(self_user))


        return [x for x in snippet_list if x.owner.id in [y for y in self.request.user.friends.friend]]


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password = password)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FriendshipList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = FriendSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
