from rest_framework import serializers
from snippets.models import Snippet, Friendship
from django.contrib.auth.models import User


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'message', 'created', 'owner')
        owner = serializers.ReadOnlyField(source='owner.username')


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all(), required=False)
    friends = serializers.PrimaryKeyRelatedField(many=True, queryset=Friendship.objects.all(), required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets', 'password', 'friends', 'first_name')
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('id', 'created', 'friend', 'approved')
        creator = serializers.ReadOnlyField(source='creator.username')
        friend = serializers.ReadOnlyField(source='friend.username')