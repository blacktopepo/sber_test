import csv
from pathlib import Path

from database import DBWriter


def write_in_file(data: list[list]) -> None:
    file_name = Path(__file__).parent.parent / 'out.csv'
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(data)
        print(f'результат выполнения в файле {file_name}')


def write_in_db(data: list[list]) -> None:
    db_writer = DBWriter()
    if db_writer.is_connect:
        db_writer.write_data(data)


def prepare_data(
    regions: list[dict],
    years: tuple[str],
    region_prefix: str
) -> list[list]:
    """Подготовка данных для записи"""
    data = [['Субъект', 'балл', *years]]
    region_name_key = f'dim{region_prefix}'
    years = [f'dim{year}' for year in years]
    for region in regions:
        years_result = []
        for el in region:
            if el == region_name_key:
                name = region[el]
            else:
                for year in years:
                    if el.startswith(year):
                        years_result.append(region[el])
        data.append(
            [name, 'балл', *years_result]
        )
    return data


def write_data(
    regions: list[dict],
    years: tuple[str],
    region_prefix: str
) -> None:
    """Записываем результаты парсинга в csv файл и БД."""
    data = prepare_data(regions, years, region_prefix)
    write_in_file(data)
    write_in_db(data)
