def chuyen_so(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0


def chuyen_so_nguyen(value):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return 0


def dinh_dang_so(value):
    try:
        so = float(value)

        if so == int(so):
            return f"{int(so):,}".replace(",", ".")

        return f"{so:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    except (ValueError, TypeError):
        return str(value)


def dinh_dang_so_ngan(value):
    so = chuyen_so(value)

    if abs(so) >= 1000000000:
        return f"{so / 1000000000:.1f} tỷ"
    if abs(so) >= 1000000:
        return f"{so / 1000000:.1f} triệu"
    if abs(so) >= 1000:
        return f"{so / 1000:.1f} nghìn"

    return dinh_dang_so(so)


def dinh_dang_tien(value):
    return dinh_dang_so(value) + " đ"
