from django.contrib import admin
from .models import Province, Channel, Post

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'province', 'platform']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['caption', 'scheduled_time', 'sent']
    filter_horizontal = ['channels']  # اجازه انتخاب چندین کانال
    exclude = ['created_by']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "channels":
            # فقط کانال‌هایی که کاربر به آن‌ها دسترسی دارد را نمایش بده
            kwargs["queryset"] = Channel.objects.filter(users=request.user)
        return super().formfield_for_manytomany(db_field, request, **kwargs)