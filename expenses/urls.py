from django.urls import path, include
from .views import ExpenseListAPIView, ExpenseDetailAPIVIew

urlpatterns = [
    path("expenses/", ExpenseListAPIView.as_view(), name="expenses"),
    path(
        "expense_detail/<int:id>/",
        ExpenseDetailAPIVIew.as_view(),
        name="expense_detail",
    ),
]
