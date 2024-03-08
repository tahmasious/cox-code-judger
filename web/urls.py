from django.urls import path
from .views import (
    submitTestCase, scorePage,get_all_test_case_tries, get_all_test_cases, get_all_test_cases_with_teams
)

urlpatterns = [
    # home page
    path('' , submitTestCase , name="submitTestCase"),
    path('scores', scorePage),
    path('all_test_case_tries', get_all_test_case_tries),
    path('all_test_cases', get_all_test_cases),
    path('all_test_cases_with_teams', get_all_test_cases_with_teams)
]
