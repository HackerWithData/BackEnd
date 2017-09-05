from backend_core.contractors.models import Contractor
from haystack import indexes

class ContractorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    license_type = indexes.CharField(model_attr='LicNum')
