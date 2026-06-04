from Calculator.common import chuyen_so, dinh_dang_so, dinh_dang_so_ngan


def tinh_tong_tien_tu_danh_sach(danh_sach):
    tong = 0

    for item in danh_sach:
        tong += chuyen_so(item.get("tongTien", 0))

    return tong


def lay_phieu_moi_nhat(danh_sach, ngay_field):
    if len(danh_sach) == 0:
        return "-"

    danh_sach_sap_xep = sorted(
        danh_sach,
        key=lambda item: str(item.get(ngay_field, "")),
        reverse=True,
    )

    return danh_sach_sap_xep[0].get(ngay_field, "-")


def dinh_dang_danh_sach_phieu(danh_sach):
    ket_qua = []

    for item in danh_sach:
        dong = dict(item)
        dong["tongTien"] = dinh_dang_so(dong.get("tongTien", 0))
        ket_qua.append(dong)

    return ket_qua


def tinh_tong_so_luong_ton(danh_sach_ton):
    tong = 0

    for item in danh_sach_ton:
        tong += chuyen_so(item.get("soLuongTon", 0))

    return int(tong)


def tinh_gia_tri_ton_kho(danh_sach_gia_tri_kho):
    tong = 0

    for item in danh_sach_gia_tri_kho:
        tong += chuyen_so(item.get("giaTriTon", 0))

    return tong


def dinh_dang_du_lieu_tong_quan(data):
    ket_qua = []

    for item in data:
        dong = dict(item)

        if isinstance(dong.get("giaTri"), (int, float)):
            dong["giaTri"] = dinh_dang_so(dong["giaTri"])

        ket_qua.append(dong)

    return ket_qua


def dinh_dang_doanh_thu_kho(data):
    ket_qua = []

    for item in data:
        dong = dict(item)
        dong["tongDoanhThu"] = dinh_dang_so(dong.get("tongDoanhThu", 0))
        ket_qua.append(dong)

    return ket_qua


def lay_doanh_thu_theo_kho(danh_sach_phieu_xuat):
    thong_ke = {}

    for item in danh_sach_phieu_xuat:
        ma_kho = item.get("maKho", "Không rõ")
        tong_tien = chuyen_so(item.get("tongTien", 0))

        if ma_kho not in thong_ke:
            thong_ke[ma_kho] = {
                "maKho": ma_kho,
                "soPhieu": 0,
                "tongDoanhThu": 0,
            }

        thong_ke[ma_kho]["soPhieu"] += 1
        thong_ke[ma_kho]["tongDoanhThu"] += tong_tien

    return sorted(
        list(thong_ke.values()),
        key=lambda item: item["tongDoanhThu"],
        reverse=True,
    )


def lay_top_5_theo_tien(danh_sach, truong_ma):
    danh_sach_sap_xep = sorted(
        danh_sach,
        key=lambda item: chuyen_so(item.get("tongTien", 0)),
        reverse=True,
    )

    ket_qua = []

    for item in danh_sach_sap_xep[:5]:
        ket_qua.append({
            "noiDung": item.get(truong_ma, ""),
            "soLuong": chuyen_so(item.get("tongTien", 0)),
        })

    return ket_qua


def lay_thong_ke_theo_thang(danh_sach, truong_ngay):
    thong_ke = {}

    for item in danh_sach:
        ngay = str(item.get(truong_ngay, ""))

        if len(ngay) >= 7:
            thang = ngay[:7]
        else:
            thang = "Không rõ"

        tong_tien = chuyen_so(item.get("tongTien", 0))
        thong_ke[thang] = thong_ke.get(thang, 0) + tong_tien

    ket_qua = []

    for thang, tong_tien in thong_ke.items():
        ket_qua.append({
            "noiDung": thang,
            "soLuong": tong_tien,
        })

    return sorted(ket_qua, key=lambda item: item["noiDung"])


def lay_top_5_ton_kho(data):
    data = sorted(
        data,
        key=lambda item: chuyen_so(item.get("soLuongTon", 0)),
        reverse=True,
    )

    ket_qua = []

    for item in data[:5]:
        ket_qua.append({
            "noiDung": item.get("tenSanPham", item.get("maSanPham", "")),
            "soLuong": chuyen_so(item.get("soLuongTon", 0)),
        })

    return ket_qua


def lay_top_5_canh_bao_ton_thap(data):
    data = sorted(
        data,
        key=lambda item: chuyen_so(item.get("canNhapThem", 0)),
        reverse=True,
    )

    ket_qua = []

    for item in data[:5]:
        ket_qua.append({
            "noiDung": item.get("tenSanPham", item.get("maSanPham", "")),
            "soLuong": chuyen_so(item.get("canNhapThem", 0)),
        })

    return ket_qua


def lay_phieu_gan_day(data, truong_ma, truong_ngay, so_luong=2):
    data = sorted(
        data,
        key=lambda item: str(item.get(truong_ngay, "")),
        reverse=True,
    )

    ket_qua = []

    for item in data[:so_luong]:
        ket_qua.append({
            "ma": item.get(truong_ma, ""),
            "ngay": item.get(truong_ngay, ""),
        })

    return ket_qua
