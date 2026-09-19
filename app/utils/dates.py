from datetime import datetime, timezone

def increase_dates(rows, fields):
    result = []
    for row in rows:
        item = dict(row)
        for field in fields:
            value = item.get(field)
            if value is None:
                continue
            # Equivalent to the Node workaround: parse DB date and add one day.
            if hasattr(value, "date") and not isinstance(value, str):
                value = value
            if hasattr(value, "date"):
                value = value.date()
            try:
                item[field] = (value + __import__("datetime").timedelta(days=1)).strftime("%d-%m-%Y")
            except Exception:
                try:
                    d = datetime.fromisoformat(str(value).replace("Z","+00:00"))
                    item[field] = (d + __import__("datetime").timedelta(days=1)).strftime("%d-%m-%Y")
                except Exception:
                    item[field] = str(value)
        result.append(item)
    return result

def count_days_between_dates(start, end):
    s = datetime.strptime(start, "%d-%m-%Y").date()
    e = datetime.strptime(end, "%d-%m-%Y").date()
    return abs((e-s).days) + 1
