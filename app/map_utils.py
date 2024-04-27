def choose_map_image(free_tables):
    # Sortowanie numerów stolików, aby nazwy plików były konsekwentne
    free_tables.sort()
    if free_tables:
        # Tworzenie nazwy pliku na podstawie wolnych stolików
        image_file = 'map_' + '_'.join(map(str, free_tables)) + '.png'
    else:
        image_file = 'map_none.png'
    return image_file
