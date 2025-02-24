from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Place

# Place 모델을 관리자로 등록
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'address')  
    search_fields = ('name', 'district')  
    list_filter = ('district',)  
    ordering = ('name',)  