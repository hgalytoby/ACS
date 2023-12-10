from app.models import MemberRecordModel, MemberModel
from app.utils.sql_query import BaseMemberChartQuery


class MemberRecordChartQuery(BaseMemberChartQuery):
    @property
    def model(self) -> type[MemberRecordModel]:
        return MemberRecordModel


class MemberChartQuery(BaseMemberChartQuery):
    @property
    def model(self) -> type[MemberModel]:
        return MemberModel
