"""backend_core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
import debug_toolbar
from users import views as userviews
from photos import views as photoview
from django.views.i18n import javascript_catalog
from django.contrib.auth.views import logout
from django.conf import settings

js_info_dict = {
    'packages': ('contractors.package',),
}
urlpatterns = [
    # admin
    url(r'^admin/', admin.site.urls),
    # home page
    url(r'^$', include('home.urls')),

    # users.urls must place before allauth urls to override
    url(r'^accounts/', include('users.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

    # dashboard
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog'),

    # search
    url(r'^search/', include('search.urls')),

    # overview
    url(r'contractor/', include('contractors.urls')),
    url(r'architect/', include('architects.urls')),
    url(r'designer/', include('designers.urls')),

    # project
    url(r'project/', include('projects.urls')),

    # transaction
    url(r'^transactions/', include('transactions.urls')),

    # url(r'^settings/password/$', userviews.password, name='password'),
    # url(r'^upload/',include('disk.urls')),
    # url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
    url(r'^reviews/', include('review.urls')),
    url(r'^rule/', include('rule.urls')),
    url(r'^career/', include('career.urls')),


]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
