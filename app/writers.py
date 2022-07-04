import csv


def write_file(data: list[list]) -> None:
    with open('out.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerows(data)


def write_data_csv(
        regions: list[dict],
        years: tuple[str],
        region_prefix: str
) -> None:
    """Записываем результаты парсинга в csv файл."""
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
    print(data)

    write_file(data)
