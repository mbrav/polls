from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):

    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def has_permission(self, request, view):

        if request.method == 'DELETE':
            return request.user and request.user.is_authenticated

        return bool(
            request.method in self.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """"
        Check object permissions
        """

        auth = bool(request.user and request.user.is_authenticated)
        if not auth:
            return request.method in self.SAFE_METHODS

        is_owner = obj.owner == request.user
        if request.method == 'DELETE':
            return is_owner or request.user.is_staff

        return bool(request.user.is_staff or is_owner)


class IsAuthenticated(permissions.IsAuthenticated):
    pass


class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method == "GET"
