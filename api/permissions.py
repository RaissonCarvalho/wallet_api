from rest_framework import permissions

class IsInvestorOwner(permissions.BasePermission):
  def has_permission(self, request, view):
    return request.user and request.user.is_authenticated

  def has_object_permission(self, request, view, transaction_obj):
    return transaction_obj.investor.user.id == request.user.id