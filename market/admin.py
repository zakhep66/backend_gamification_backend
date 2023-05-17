from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from market.models import StoreHistory, StoreProduct
from .admin_resources import StoreProductResource, StoreHistoryResource


@admin.register(StoreProduct)
class StoreProductAdmin(ImportExportModelAdmin):
	resource_class = StoreProductResource


@admin.register(StoreHistory)
class StoreHistoryAdmin(ImportExportModelAdmin):
	resource_class = StoreHistoryResource
