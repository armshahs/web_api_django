from django.urls import path, include
from .views import IncomeListAPIView, IncomeDetailAPIVIew

urlpatterns = [
    path("incomes/", IncomeListAPIView.as_view(), name="incomes"),
    path(
        "income_detail/<int:id>/",
        IncomeDetailAPIVIew.as_view(),
        name="income_detail",
    ),
]
