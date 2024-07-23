import symbols

def transform(records):
    for data in records:
        data.value['s'] = symbols.PAIRS[data.value['s']]
    return records

