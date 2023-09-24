from datetime import datetime, date
from typing import Optional
from fastapi import Query

from app.models import MemberModel, MemberRecordModel
from app.utils.enums import BloodType
from app.utils.sql_query import BaseQuery, QuerySql, SortSql


class MemberRecordQuery(BaseQuery):
    def __init__(
            self,
            status: Optional[bool] = Query(
                default=None,
                description='進出入狀態',
                alias='status',
            ),
            member_location_name: Optional[str] = Query(
                default=None,
                description='成員地點名字',
                alias='memberLocationName',
            ),
            member_name: Optional[str] = Query(
                default=None,
                description='成員名字',
                alias='memberName',
            ),
            member_phone: Optional[str] = Query(
                default=None,
                description='成員手機',
                regex=r'09\d{8}$',
                alias='memberPhone',
            ),
            member_company: Optional[str] = Query(
                default=None,
                description='成員公司',
                alias='memberCompany',
            ),
            member_job_title: Optional[str] = Query(
                default=None,
                description='成員職稱',
                alias='memberJobTitle',
            ),
            created_at: Optional[tuple[datetime | date, datetime | date]] = Query(
                default=None,
                description='創建日期',
                alias='createdAt',
            ),
            status_num: Optional[int] = Query(
                default=None,
                description='排序進出入順序',
                alias='statusNum',
            ),
            member_company_num: Optional[int] = Query(
                default=None,
                description='排序成員公司順序',
                alias='memberCompanyNum',
            ),
            member_job_title_num: Optional[int] = Query(
                default=None,
                description='排序成員職稱順序',
                alias='memberJosTitleNum',
            ),
            member_location_name_num: Optional[int] = Query(
                default=None,
                description='排序成員地點順序',
                alias='memberLocationNameNum',
            ),
            member_name_num: Optional[int] = Query(
                default=None,
                description='排序成員名字順序',
                alias='memberNameNum',
            ),
            member_phone_num: Optional[int] = Query(
                default=None,
                description='排序成員手機順序',
                alias='memberPhoneNum',
            ),
            created_at_num: Optional[int] = Query(
                default=None,
                description='排序創建日期順序',
                alias='createdAtNum',
            ),
            status_sort: Optional[bool] = Query(
                default=None,
                description='排序進出入',
                alias='statusSort',
            ),
            member_location_name_sort: Optional[bool] = Query(
                default=None,
                description='排序成員地點',
                alias='memberLocationNameSort',
            ),
            member_name_sort: Optional[bool] = Query(
                default=None,
                description='排序成員名字',
                alias='memberNameSort',
            ),
            member_phone_sort: Optional[bool] = Query(
                default=None,
                description='排序成員手機',
                alias='memberPhoneSort',
            ),
            member_job_title_sort: Optional[bool] = Query(
                default=None,
                description='排序成員職稱',
                alias='memberJobTitleSort',
            ),
            member_company_sort: Optional[bool] = Query(
                default=None,
                description='排序成員公司',
                alias='memberCompanySort',
            ),
            created_at_sort: Optional[bool] = Query(
                default=None,
                description='排序創建日期',
                alias='createdAtSort',
            ),
    ):
        super(MemberRecordQuery, self).__init__()
        self.query_list.extend([
            QuerySql(
                expression=MemberRecordModel.member_name.ilike(f'%{member_name}%'),
                value=member_name,
                include_none=False,
            ),
            QuerySql(
                expression=MemberRecordModel.member_phone.ilike == member_phone,
                value=member_phone,
                include_none=False,
            ),
            QuerySql(
                expression=MemberRecordModel.member_company.ilike == member_company,
                value=member_company,
                include_none=False,
            ),
            QuerySql(
                expression=MemberRecordModel.member_job_title.ilike == member_job_title,
                value=member_job_title,
                include_none=False,
            ),
            QuerySql(
                expression=MemberRecordModel.status == status,
                value=status,
                include_none=False,
            ),
            QuerySql(
                expression=MemberRecordModel.member_location_name.ilike == member_location_name,
                value=member_location_name,
                include_none=False,
            ),
        ])
        self.convert_datetime_to_query(
            date_arr=created_at,
            sql_field=MemberRecordModel.created_at,
        )
        self.sort_list.extend([
            SortSql(
                sql_field=MemberRecordModel.member_name,
                sort=member_name_sort,
                num=member_name_num,
            ),
            SortSql(
                sql_field=MemberRecordModel.member_phone,
                sort=member_phone_sort,
                num=member_phone_num,
            ),
            SortSql(
                sql_field=MemberRecordModel.member_company,
                sort=member_company_sort,
                num=member_company_num,
            ),
            SortSql(
                sql_field=MemberRecordModel.member_job_title,
                sort=member_job_title_sort,
                num=member_job_title_num,
            ),
            SortSql(
                sql_field=MemberRecordModel.status,
                sort=status_sort,
                num=status_num,
            ),
            SortSql(
                sql_field=MemberRecordModel.member_location_name,
                sort=member_location_name_sort,
                num=member_location_name_num,
            ),
            SortSql(
                sql_field=MemberRecordModel.created_at,
                sort=created_at_sort,
                num=created_at_num,
            ),
        ])


class MemberQuery(BaseQuery):
    def __init__(
            self,
            name: Optional[str] = Query(
                default=None,
                description='名字',
                max_length=32,
            ),
            blood_type: BloodType = Query(
                default=None,
                description='血型',
                alias='bloodType',
            ),
            company: Optional[str] = Query(
                default=None,
                description='公司',
                max_length=32,
            ),
            job_title: Optional[str] = Query(
                default=None,
                description='職稱',
                max_length=32,
                alias='jobTitle',
            ),
            created_at: Optional[tuple[datetime | date, datetime | date]] = Query(
                default=None,
                description='創建日期',
                alias='createdAt',
            ),
            updated_at: Optional[tuple[datetime | date, datetime | date]] = Query(
                default=None,
                description='結束日期',
                alias='updateAt',
            ),
            birthday: Optional[tuple[datetime | date, datetime | date]] = Query(
                default=None,
                description='生日',
                alias='birthday',
            ),
            phone: Optional[str] = Query(
                default=None,
                description='手機號碼',
                regex=r'09\d{8}$',
            ),
            name_num: Optional[int] = Query(
                default=None,
                description='排序名字順序',
                alias='nameNum',
            ),
            blood_type_num: Optional[int] = Query(
                default=None,
                description='排序血型順序',
                alias='bloodTypeNum',
            ),
            birthday_num: Optional[int] = Query(
                default=None,
                description='排序生日順序',
                alias='birthdayNum',
            ),
            phone_num: Optional[int] = Query(
                default=None,
                description='排序手機順序',
                alias='phoneNum',
            ),
            company_num: Optional[int] = Query(
                default=None,
                description='排序公司順序',
                alias='companyNum',
            ),
            job_title_num: Optional[int] = Query(
                default=None,
                description='排序職稱順序',
                alias='jobTitleNum',
            ),
            created_at_num: Optional[int] = Query(
                default=None,
                description='排序創建日期順序',
                alias='createdAtNum',
            ),
            updated_at_num: Optional[datetime] = Query(
                default=None,
                description='排序更新結束順序',
                alias='updatedAtNum',
            ),
            name_sort: Optional[int] = Query(
                default=None,
                description='排序名字順序',
                alias='nameNumSort',
            ),
            blood_type_sort: Optional[bool] = Query(
                default=None,
                description='排序血型',
                alias='bloodTypeSort',
            ),
            birthday_sort: Optional[bool] = Query(
                default=None,
                description='排序生日',
                alias='birthdaySort',
            ),
            company_sort: Optional[bool] = Query(
                default=None,
                description='排序公司',
                alias='companySort',
            ),
            job_title_sort: Optional[bool] = Query(
                default=None,
                description='排序職稱',
                alias='jobTitleSort',
            ),
            phone_sort: Optional[bool] = Query(
                default=None,
                description='排序手機',
                alias='phoneSort',
            ),
            created_at_sort: Optional[bool] = Query(
                default=None,
                description='排序創建日期',
                alias='createdAtSort',
            ),
            updated_at_sort: Optional[bool] = Query(
                default=None,
                description='排序更新日期',
                alias='updatedAtSort',
            ),
    ):
        super(MemberQuery, self).__init__()
        self.query_list.extend([
            QuerySql(
                expression=MemberModel.name.ilike(f'%{name}%'),
                value=name,
                include_none=False,
            ),
            QuerySql(
                expression=MemberModel.blood_type == blood_type,
                value=blood_type,
                include_none=False,
            ),
            QuerySql(
                expression=MemberModel.phone.ilike(f'%{phone}%'),
                value=phone,
                include_none=False,
            ),
            QuerySql(
                expression=MemberModel.company.ilike(f'%{company}%'),
                value=company,
                include_none=False,
            ),
            QuerySql(
                expression=MemberModel.job_title.ilike(f'%{job_title}%'),
                value=job_title,
                include_none=False,
            ),
        ])
        self.convert_datetime_to_query(
            date_arr=birthday,
            sql_field=MemberModel.birthday,
        )
        self.convert_datetime_to_query(
            date_arr=created_at,
            sql_field=MemberModel.created_at,
        )
        self.convert_datetime_to_query(
            date_arr=updated_at,
            sql_field=MemberModel.updated_at,
        )
        self.sort_list.extend([
            SortSql(
                sql_field=MemberModel.name,
                sort=name_sort,
                num=name_num,
            ),
            SortSql(
                sql_field=MemberModel.blood_type,
                sort=blood_type_sort,
                num=blood_type_num,
            ),
            SortSql(
                sql_field=MemberModel.birthday,
                sort=birthday_sort,
                num=birthday_num,
            ),
            SortSql(
                sql_field=MemberModel.phone,
                sort=phone_sort,
                num=phone_num,
            ),
            SortSql(
                sql_field=MemberModel.company,
                sort=company_sort,
                num=company_num,
            ),
            SortSql(
                sql_field=MemberModel.job_title,
                sort=job_title_sort,
                num=job_title_num,
            ),
            SortSql(
                sql_field=MemberModel.created_at,
                sort=created_at_sort,
                num=created_at_num,
            ),
            SortSql(
                sql_field=MemberModel.updated_at,
                sort=updated_at_sort,
                num=updated_at_num,
            ),
        ])
