from rest_framework import serializers
from snippets.models import Snippet, Friendship
from django.contrib.auth.models import User
import time
import datetime


class UnixEpochDateField(serializers.DateTimeField):

    def to_representation(self, value):
        """ Return epoch time for a datetime object or ``None``"""
        import time
        try:
            return int(time.mktime(value.timetuple()))
        except (AttributeError, TypeError):
            return None

    def to_internal_value(self, value):
        import datetime
        return datetime.datetime.fromtimestamp(int(value))


class SnippetSerializer(serializers.ModelSerializer):
    starttime = UnixEpochDateField(source='created', required=False)
    owner = serializers.ReadOnlyField(source='owner.username', required=False)

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'message', 'starttime', 'owner')



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