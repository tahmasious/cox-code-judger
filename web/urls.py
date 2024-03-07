from django.urls import path
from .views import (
    submitTestCase, scorePage,read_from_file
)

urlpatterns = [
    # home page
    path('' , submitTestCase , name="submitTestCase"),
    path('scores', scorePage),
    path('test', read_from_file ),
]
