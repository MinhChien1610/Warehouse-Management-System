def tinh_chenh_lech_kiem_ke(so_luong_he_thong, so_luong_thuc_te):
    return chuyen_so_nguyen(so_luong_thuc_te) - chuyen_so_nguyen(so_luong_he_thong)


def chuyen_so_nguyen(value):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return 0
