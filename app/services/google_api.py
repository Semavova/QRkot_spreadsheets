from aiogoogle import Aiogoogle
from datetime import datetime, timedelta
from copy import deepcopy
from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
SHEETS_VERSION = 'v4'
DRIVE_VERSION = 'v3'
ROW_COUNT = 100
COLUMN_COUNT = 3

SHEET_BODY = dict(
    properties=dict(title='', locale='ru_RU'),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(rowCount=ROW_COUNT, columnCount=COLUMN_COUNT)
    ))]
)
SHEET_TITLE = 'Отчет на {datetime}'
PERMISSIONS_BODY = dict(
    type='user', role='writer', emailAddress=settings.email
)
SHEET_HEAD = [
    ['Отчет от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
SHEET_SIZE_ERROR = (
    f'В созданной таблице {ROW_COUNT} строк и {COLUMN_COUNT} столбцов. '
    'Данным требуется {row} строк и {column} столбцов.'
)
RANGE = 'R1C1:R{row}C{column}'
VALUE_INPUT_OPTION = 'USER_ENTERED'
MAJOR_DIMENSION = 'ROWS'


async def spreadsheets_create(
    wrapper_services: Aiogoogle,
) -> str:
    service = await wrapper_services.discover('sheets', SHEETS_VERSION)
    spreadsheet_body = deepcopy(SHEET_BODY)
    spreadsheet_body['properties']['title'] = SHEET_TITLE.format(
        datetime=datetime.now().strftime(FORMAT)
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', DRIVE_VERSION)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSIONS_BODY,
            fields="id"
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', SHEETS_VERSION)
    header = deepcopy(SHEET_HEAD)
    header[0][1] = datetime.now().strftime(FORMAT)
    table_values = [
        *header,
        *[[str(name), str(timedelta(time)), str(description)]
          for name, time, description in projects]
    ]
    row_count = len(table_values)
    column_count = max(map(len, header))
    if row_count > ROW_COUNT or column_count > COLUMN_COUNT:
        raise ValueError(
            SHEET_SIZE_ERROR.format(row=row_count, column=column_count)
        )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=RANGE.format(row=row_count, column=column_count),
            valueInputOption=VALUE_INPUT_OPTION,
            json={
                'majorDimension': MAJOR_DIMENSION,
                'values': table_values
            }
        )
    )
