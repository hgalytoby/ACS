from datetime import date, datetime
from typing import Protocol

from app.schemas.chart import BaseGrowthRead


class DatedModel(Protocol):
    created_at: datetime


class DateGrowthChart:
    @classmethod
    def get_default_monthly_counts(cls, start_date: date, end_date: date) -> dict[str, int]:
        num_months = 12 * (end_date.year - start_date.year) + end_date.month - start_date.month + 1
        start_date = start_date.replace(day=1)
        counts = {}
        for _ in range(num_months):
            counts[f'{start_date.year}-{start_date.month}'] = 0
            if start_date.month == 12:
                start_date = start_date.replace(year=start_date.year + 1, month=1)
            else:
                start_date = start_date.replace(month=start_date.month + 1)
        return counts

    @classmethod
    def update_monthly_counts(cls, counts: dict[str, int], items: list[DatedModel]):
        for item in items:
            counts[f'{item.created_at.year}-{item.created_at.month}'] += 1

    @classmethod
    def accumulate_counts(cls, counts: dict[str, int]):
        accumulated = 0
        for month in counts:
            counts[month] += accumulated
            accumulated = counts[month]

    @classmethod
    def get_monthly_growth(cls, counts: dict[str, int]) -> list[BaseGrowthRead]:
        growth = []
        for month, count in counts.items():
            year, month = month.split('-')
            growth.append(BaseGrowthRead(
                date=date(
                    year=int(year),
                    month=int(month),
                    day=1,
                ),
                count=count
            ))
        return growth

    @classmethod
    def calculate_date_growth(
            cls,
            start_date: date,
            end_date: date,
            accumulate: bool,
            items: list[DatedModel],
    ) -> list[BaseGrowthRead]:
        counts = cls.get_default_monthly_counts(
            start_date=start_date,
            end_date=end_date,
        )
        cls.update_monthly_counts(counts=counts, items=items)
        if accumulate:
            cls.accumulate_counts(counts=counts)
        growth = cls.get_monthly_growth(counts=counts)
        return growth
