import urllib

from contractors.models import Contractor


# Ajax POST request
def search_by_address_object(request):
    zipcode = int(request['address']['address_components'][6]['short_name'])
    target = request['target']
    query_set = Contractor.objects.filter(PosCode=zipcode).filter(LicType__icontains=target)
    return query_set


# Ajax POST request
def search_by_address_object_redirect_url(request):
    print request
    zipcode = int(request['address']['address_components'][6]['short_name'])
    target = request['target']
    url_parameters = {
        'zipcode': zipcode,
        'target': target
    }
    return urllib.urlencode(url_parameters)


# GET request
def search_by_zipcode(request):
    target = request.GET['target']
    zipcode = request.GET['zipcode']
    query_set = Contractor.objects.filter(PosCode=zipcode).filter(LicType__icontains=target)
    return query_set
