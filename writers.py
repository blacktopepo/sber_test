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





if __name__ == '__main__':
    print(get_keys_years(
        {
            "dim0": "Средний индекс качества городской среды по Российской Федерации (субъекту Российской Федерации) за отчетный год, в баллах (округляется до целого значения)",
            "dim3301": "Российская Федерация",
            "dim30611": "балл",
            "dim2018_1558883_d77585884_i2184": "163",
            "dim2019_1558883_d77585884_i2185": "169",
            "dim2020_1558883_d77585884_i2195": "177"
        },
        ('2018', '2019', '2020')
    ))

