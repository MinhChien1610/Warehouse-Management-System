def thong_ke_tien_theo_ngay(danh_sach_phieu, truong_ngay):
    thong_ke = {}

    for phieu in danh_sach_phieu:
        ngay = phieu.get(truong_ngay, "Kh?ng r?")
        tong_tien = chuyen_so_nguyen(phieu.get("tongTien", 0))
        thong_ke[ngay] = thong_ke.get(ngay, 0) + tong_tien

    return {
        "data": danh_sach_phieu,
        "labels": list(thong_ke.keys()),
        "values": list(thong_ke.values()),
        "tongPhieu": len(danh_sach_phieu),
        "soNgay": len(thong_ke),
        "tongTien": sum(thong_ke.values()),
    }


def chuyen_so_nguyen(value):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return 0
