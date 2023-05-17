from import_export import resources

from .models import StoreProduct, StoreHistory


class StoreProductResource(resources.ModelResource):
	class Meta:
		model = StoreProduct


class StoreHistoryResource(resources.ModelResource):
	class Meta:
		model = StoreHistory
