import symbols

def transform(records):
    try:
        for data in records:
            data = data.value
            data['s'] = symbols.PAIRS[data['s']]
        return records
    except Exception as e:
        print(f"Error: {e}")
