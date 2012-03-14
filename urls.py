import os
DIRNAME = os.path.dirname(__file__)

from django.conf.urls.defaults import *

import data_tables

# Look in all installed apps for dt_forms
data_tables.autodiscover()

urlpatterns = patterns(
    'data_tables.views',
    (r'^ajax_get_records/?$', 'ajax_get_records'),
)
