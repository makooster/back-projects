from rest_framework import permissions

class RolePermission(permissions.BasePermission):
    required_role = None  # Default is None

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == self.required_role

class IsAdmin(RolePermission):
    required_role = "admin"

class IsTrader(RolePermission):
    required_role = "trader"

class IsSalesRep(RolePermission):
    required_role = "sales_rep"
