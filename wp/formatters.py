def color_map(val):
    if val > 0:
        return 'color: green;'
    elif val < 0:
        return 'color: red;'

def delta_format(val):
    if val > 0:
        return f"⬆ {val:.2f}"
    if val < 0:
        return f"⬇ {val:.2f}"
    return f"{val:.2f}"