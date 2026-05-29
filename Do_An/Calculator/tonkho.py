def tinh_tong_ton_kho(danh_sach_ton):
    tong = 0

    for item in danh_sach_ton:
        tong += chuyen_so_nguyen(item.get("soLuongTon", 0))

    return int(tong)


def tinh_ton_kho_theo_kho(danh_sach_kho, danh_sach_ton):
    thong_ke = {}

    for kho in danh_sach_kho:
        ma_kho = kho.get("maKho", "")
        thong_ke[ma_kho] = {
            "maKho": ma_kho,
            "tenKho": kho.get("tenKho", ma_kho),
            "tongTon": 0,
        }

    for ton in danh_sach_ton:
        ma_kho = ton.get("maKho", "")
        so_luong = chuyen_so_nguyen(ton.get("soLuongTon", 0))

        if ma_kho not in thong_ke:
            thong_ke[ma_kho] = {
                "maKho": ma_kho,
                "tenKho": ma_kho,
                "tongTon": 0,
            }

        thong_ke[ma_kho]["tongTon"] += so_luong

    return list(thong_ke.values())


def lay_canh_bao_ton_thap(danh_sach_ton, danh_sach_san_pham):
    ket_qua = []

    for ton in danh_sach_ton:
        ma_san_pham = ton.get("maSanPham", "")
        san_pham = tim_san_pham_trong_danh_sach(danh_sach_san_pham, ma_san_pham)

        if san_pham is None:
            continue

        so_luong_ton = chuyen_so_nguyen(ton.get("soLuongTon", 0))
        muc_toi_thieu = chuyen_so_nguyen(san_pham.get("mucTonToiThieu", 0))

        if so_luong_ton < muc_toi_thieu:
            ket_qua.append({
                "maKho": ton.get("maKho", ""),
                "maSanPham": ma_san_pham,
                "tenSanPham": san_pham.get("tenSanPham", ""),
                "soLuongTon": so_luong_ton,
                "mucTonToiThieu": muc_toi_thieu,
                "canNhapThem": muc_toi_thieu - so_luong_ton,
            })

    return ket_qua


def tinh_tong_so_luong_can_nhap(danh_sach):
    tong = 0

    for item in danh_sach:
        tong += chuyen_so_nguyen(item.get("canNhapThem", 0))

    return int(tong)


def tim_san_pham_trong_danh_sach(danh_sach_san_pham, ma_san_pham):
    for san_pham in danh_sach_san_pham:
        if san_pham.get("maSanPham") == ma_san_pham:
            return san_pham

    return None


def chuyen_so_nguyen(value):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return 0
