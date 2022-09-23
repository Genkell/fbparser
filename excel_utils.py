import datetime

import xlwt


def create_table(d: list) -> str:
    wb = xlwt.Workbook()
    ws = wb.add_sheet('List 1')
    ws.write(0, 0, "Ссылка группы")
    ws.write(0, 1, "Статус группы")
    ws.write(0, 2, "Количество участников")
    ws.write(0, 3, "Название группы")
    ws.write(0, 4, "Информация о публикации")
    for group in d:
        ws.write(1 + d.index(group), 0, group["link"])
        ws.write(1 + d.index(group), 1, group["type"])
        ws.write(1 + d.index(group), 2, group["members"])
        ws.write(1 + d.index(group), 3, group["name"])
        ws.write(1 + d.index(group), 4, group["frequency"])
    name = f"result_{datetime.datetime.now().timestamp()}.xls"
    wb.save(name)
    return name
