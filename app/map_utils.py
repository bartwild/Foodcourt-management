def choose_sector_image(free_tables, sector):
    # Sortowanie numerów stolików, aby nazwy plików były konsekwentne
    free_tables.sort()
    if free_tables:
        # Tworzenie nazwy pliku na podstawie wolnych stolików
        image_file = 'map_' + '_'.join(map(str, free_tables)) + f'_s{sector}' + '.png'
        image_file = image_file.replace(':', "_")
    else:
        image_file = 'map_' + f's{sector}' + '.png'
    return image_file


def choose_total_image(free_tables_per_sector):
    image_filename = "map_" + "_".join([f"{sector}:{free_tables}" for sector, free_tables in sorted(free_tables_per_sector.items())])
    image_filename = image_filename.replace(':', "_")
    image_filename += ".png"
    return image_filename


def get_free_tables_per_sector(table_status):
    free_tables_per_sector = {}
    for _, info in table_status.items():
        sector = info['sector']
        if sector not in free_tables_per_sector:
            free_tables_per_sector[sector] = 0
        if info['status'] == 'free':
            free_tables_per_sector[sector] += 1
    return free_tables_per_sector
