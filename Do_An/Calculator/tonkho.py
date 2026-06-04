from Calculator.common import chuyen_so, chuyen_so_nguyen


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


def lap_du_lieu_ton_kho(danh_sach_ton, danh_sach_san_pham, danh_sach_vi_tri=None):
    danh_sach_vi_tri = danh_sach_vi_tri or []
    ket_qua = []

    for ton in danh_sach_ton:
        ma_san_pham = lay_gia_tri(ton, "maSanPham", "maSP")
        san_pham = tim_san_pham_trong_danh_sach(danh_sach_san_pham, ma_san_pham)
        so_luong_ton = chuyen_so(ton.get("soLuongTon", ton.get("soLuong", 0)))

        if san_pham is None:
            san_pham = {}

        muc_ton_toi_thieu = chuyen_so(san_pham.get("mucTonToiThieu", ton.get("mucTonToiThieu", 0)))
        don_gia = chuyen_so(san_pham.get("donGia", ton.get("donGia", 0)))
        trang_thai = "Tồn thấp" if so_luong_ton < muc_ton_toi_thieu else "Ổn định"

        ket_qua.append({
            "maKho": ton.get("maKho", ton.get("maCN", "")),
            "maSanPham": ma_san_pham,
            "tenSanPham": san_pham.get("tenSanPham", ton.get("tenSanPham", "")),
            "soLuongTon": int(so_luong_ton),
            "donGia": int(don_gia),
            "giaTriTon": int(so_luong_ton * don_gia),
            "mucTonToiThieu": int(muc_ton_toi_thieu),
            "trangThai": trang_thai,
            "canhBao": trang_thai,
            "viTriHang": lay_vi_tri_hang(ton, danh_sach_vi_tri),
        })

    return ket_qua


def lay_canh_bao_ton_thap(danh_sach_ton, danh_sach_san_pham, danh_sach_vi_tri=None):
    ket_qua = []

    for item in lap_du_lieu_ton_kho(danh_sach_ton, danh_sach_san_pham, danh_sach_vi_tri):
        so_luong_ton = chuyen_so_nguyen(item.get("soLuongTon", 0))
        muc_toi_thieu = chuyen_so_nguyen(item.get("mucTonToiThieu", 0))

        if so_luong_ton < muc_toi_thieu:
            dong = dict(item)
            dong["canNhapThem"] = muc_toi_thieu - so_luong_ton
            ket_qua.append(dong)

    return ket_qua


def lay_du_lieu_gia_tri_kho(danh_sach_ton, danh_sach_san_pham):
    return [
        {
            "maKho": item.get("maKho", ""),
            "maSanPham": item.get("maSanPham", ""),
            "tenSanPham": item.get("tenSanPham", ""),
            "soLuongTon": item.get("soLuongTon", 0),
            "donGia": item.get("donGia", 0),
            "giaTriTon": item.get("giaTriTon", 0),
        }
        for item in lap_du_lieu_ton_kho(danh_sach_ton, danh_sach_san_pham)
    ]


def tinh_tong_so_luong_can_nhap(danh_sach):
    tong = 0

    for item in danh_sach:
        tong += chuyen_so_nguyen(item.get("canNhapThem", 0))

    return int(tong)


def tim_san_pham_trong_danh_sach(danh_sach_san_pham, ma_san_pham):
    for san_pham in danh_sach_san_pham:
        if san_pham.get("maSanPham", san_pham.get("maSP", "")) == ma_san_pham:
            return san_pham

    return None


def lay_gia_tri(item, *keys):
    for key in keys:
        gia_tri = item.get(key, "")

        if gia_tri != "":
            return gia_tri

    return ""


def lay_vi_tri_hang(ton, danh_sach_vi_tri):
    ma_vi_tri = lay_gia_tri(
        ton,
        "maViTri",
        "ma_vi_tri",
        "viTriHang",
        "vi_tri_hang",
        "viTri",
        "vi_tri",
    )

    if ma_vi_tri != "":
        return ma_vi_tri

    for vi_tri in danh_sach_vi_tri:
        if vi_tri.get("maKho") == ton.get("maKho", ""):
            return vi_tri.get("maViTri", "")

    return ""
