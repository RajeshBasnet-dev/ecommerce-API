from rest_framework import permissions

class IsBuyer(permissions.BasePermission):
    """
    Custom permission to only allow buyers to access the view.
    """
    
    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
        # Check if user has buyer role
        return getattr(request.user, 'role', None) == 'buyer'

class IsSeller(permissions.BasePermission):
    """
    Custom permission to only allow sellers to access the view.
    """
    
    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
        # Check if user has seller role
        return getattr(request.user, 'role', None) == 'seller'

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins to access the view.
    """
    
    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
        # Check if user has admin role
        return getattr(request.user, 'role', None) == 'admin'

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Admins can access everything
        if getattr(request.user, 'role', None) == 'admin':
            return True
        
        # Check if user is the owner of the object
        # This assumes the object has a 'user' attribute pointing to the owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # For objects that might have different owner field names
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
            
        return False

class IsSellerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow sellers or admins to access the view.
    """
    
    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
        # Check if user has seller or admin role
        user_role = getattr(request.user, 'role', None)
        return user_role in ['seller', 'admin']

class IsBuyerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow buyers or admins to access the view.
    """
    
    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
        # Check if user has buyer or admin role
        user_role = getattr(request.user, 'role', None)
        return user_role in ['buyer', 'admin']