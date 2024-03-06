from django.urls import path
from .views import (
    submitTestCase, scorePage
)

urlpatterns = [
    # home page
    path('' , submitTestCase , name="submitTestCase"),
    path('scores', scorePage)
]
