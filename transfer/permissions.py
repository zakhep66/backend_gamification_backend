from rest_framework import permissions

from users.models import Student


class IsStudent(permissions.BasePermission):
    """
     Разрешает доступ только пользователям, которые являются экземплярами модели Student.
     """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                return isinstance(request.user.student, Student)
            except Student.DoesNotExist:
                return False
        return False
