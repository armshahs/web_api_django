from .views import ExpenseSummaryStats, IncomeSummaryStats
from django.urls import path

urlpatterns = [
    path(
        "expenses_category_data/",
        ExpenseSummaryStats.as_view(),
        name="expense-category-summary",
    ),
    path(
        "incomes_source_data/",
        IncomeSummaryStats.as_view(),
        name="income-source-summary",
    ),
]
