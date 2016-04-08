from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class IsOwnerOrFriend(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return (
            (request.method in permissions.SAFE_METHODS and
             (obj.owner in request.user.friends) and
             request.user.is_authenticated)
            or
            # Write permissions are only allowed to the owner of the snippet.
            (request.user and
            obj.owner == request.user and
            request.user.is_authenticated())
        )

