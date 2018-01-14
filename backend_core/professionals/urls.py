from django.conf.urls import url

from views import ProfessionalView


urlpatterns = [
    url(r'^([0-9]{0,32})/$', ProfessionalView.as_view(), name='professional'),
]
