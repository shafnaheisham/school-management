from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,FeesManagement,Student,StudentFeesHistory,LibraryBookLendingHistory,LibraryBookRegister

# class UserAdmin(BaseUserAdmin):
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('full_name',)}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2'),
#         }),
#     )
#     list_display = ('email', 'is_staff', 'is_superuser')
#     search_fields = ('email',)
#     ordering = ('email',)

# Register your models here.
admin.site.register(User)
admin.site.register(FeesManagement)
admin.site.register(Student)
admin.site.register(LibraryBookRegister)
admin.site.register(StudentFeesHistory)
admin.site.register(LibraryBookLendingHistory)