from rest_framework import permissions


class AdminUserOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_superuser and request.user)
    
    
class ReviewUserOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True 
        return obj.review_user == request.user