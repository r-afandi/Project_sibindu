from django.contrib import admin
from ..models.data_suspek.m_data_suspek import DataSuspek


class DataSuspekAdmin(admin.ModelAdmin):
    list_display = DataSuspek,
    list_filter = ('diagnosa',)
    search_fields = ('nama', 'alamat', 'petugas_id')

    # Menampilkan tombol "Add" hanya untuk petugas
    def has_add_permission(self, request):
        return request.user.groups.filter(name='Petugas').exists()

    # Menampilkan tombol "Delete" hanya untuk petugas
    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='Petugas').exists()

admin.site.register(DataSuspek, DataSuspekAdmin)