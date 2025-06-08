from rest_framework import permissions

class HasChannelAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        # اگر کاربر admin باشد، همه دسترسی‌ها را بده
        if request.user.is_superuser:
            return True

        channel_id = request.query_params.get('channel')
        author_id = request.query_params.get('author')

        # چک کنیم کاربر به این channel دسترسی دارد یا خیر
        if channel_id:
            if not request.user.userchannelaccess_set.filter(channel_id=channel_id).exists():
                return False

        if author_id:
            if not request.user.userauthormodelaccess_set.filter(author_id=author_id).exists():
                return False

        return True