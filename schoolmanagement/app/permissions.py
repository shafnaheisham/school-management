from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users (superusers).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'administrator'


class OfficeStaffPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type== 'office_staff'

class IsLibrarian(BasePermission):
    """
    Custom permission to allow only librarians to add books.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'librarian'