from haystack import indexes
from haystack import site
from models import Contractor


class ContractorIndex(indexes.SearchIndex, indexes.Indexable):
    # TODO: add more field corresponding to Contractor model
    text = indexes.CharField(document=True, use_template=True)
    inc_name = indexes.CharField(model_attr='BusName')
    license_num = indexes.IntegerField(model_attr='LicNum')
    license_type = indexes.CharField(model_attr='LicType')
    zipcode = indexes.IntegerField(model_attr='PosCode')

    def get_model(self):
        return Contractor

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

site.register(Contractor, ContractorIndex)
