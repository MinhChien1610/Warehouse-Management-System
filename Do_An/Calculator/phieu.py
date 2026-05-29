def tinh_tong_tien_chi_tiet(chi_tiet):
    tong = 0

    for item in chi_tiet:
        so_luong = chuyen_so_nguyen(item.get("soLuong", 0))
        don_gia = chuyen_so_nguyen(item.get("donGia", 0))
        tong += so_luong * don_gia

    return tong


def chuyen_so_nguyen(value):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return 0
