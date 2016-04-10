from snippets.models import Snippet, Friendship
from rest_framework import generics
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer, SnippetSerializer, FriendSerializer
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly, IsOwnerOrFriend
from django.contrib.auth.hashers import make_password


class SnippetList(generics.ListCreateAPIView):
    permission_classes = (IsOwnerOrFriend,)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        snippet_list = Snippet.objects.all()
        friends = Friendship.objects.filter(creator = self.request.user.id)
        return [x for x in snippet_list
                if ((x.owner.id in [y.friend.id for y in
                                    [z for z in friends if z.approved == True]]) or
                    (x.owner.id == self.request.user.id))
                ]


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
    queryset = Friendship.objects.all()

    def perform_create(self, serializer):

        queryset = Friendship.objects.filter(creator = self.request.user).filter(friend = self.request.data['friend'])
        revqueryset = Friendship.objects.filter(creator=self.request.data['friend']).filter(friend=self.request.user)
        if (not queryset) and (revqueryset):
            serializer.save(creator = self.request.user, approved = True)
            revqueryset[0].approved = True
            revqueryset[0].save()
        elif (not queryset) and (not revqueryset):
            serializer.save(creator=self.request.user)


class UserLogin(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
