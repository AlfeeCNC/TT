"""TriggerToken URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog
from Club.views import landingPage
from MemberSystem.views import PaymentReturnView

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('MemberSystem', 'Club'),  # my app name
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('backstage/', include('BackStage.urls')),
]

urlpatterns += i18n_patterns(
    # path(<your_path>, include(('<your_app>.urls', '<your_app>')),
    path('', landingPage, name='landingPage'),
    path('clubs/', include('Club.urls')),
    path('members/', include('MemberSystem.urls')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog')
)
