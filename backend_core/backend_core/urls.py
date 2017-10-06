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

js_info_dict = {
    'packages': ('contractors.package',),
}
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # home page
    url(r'^$', include('home.urls')),
    # # sign up
    # url(r'^signup/', include('users.urls')),
    # # login
    # url(r'^login/$', auth_views.login, name='login'),
    # # log out
    # url(r'^logout/$', auth_views.logout, {'next_page': 'home_index'}, name='logout'),
    # # password reset
    # url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    # url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     auth_views.password_reset_confirm, name='password_reset_confirm'),
    # url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    # url(r'^oauth/', include('social_django.urls', namespace='social')),
    # url(r'settings/$', userviews.settings, name='settings'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/', include('users.urls')),

    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog'),

    # search
    url(r'^search/', include('search.urls')),
    url(r'contractor/', include('contractors.urls')),
    #url(r'^settings/password/$', userviews.password, name='password'),
    #url(r'^upload/',include('disk.urls')),
    #url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
    #url(r'^reviews/', include('review.urls')),
    url(r'^rule/', include('rule.urls')),
    url(r'^career/', include('career.urls'))
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)