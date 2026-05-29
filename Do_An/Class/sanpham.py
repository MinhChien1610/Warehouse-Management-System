class SanPham:
    def __init__(self, ma_san_pham, ten_san_pham, ma_don_vi_tinh, ma_loai_hang, don_gia, muc_ton_toi_thieu, trang_thai="Đang kinh doanh"):
        self.ma_san_pham = ma_san_pham
        self.ten_san_pham = ten_san_pham
        self.ma_don_vi_tinh = ma_don_vi_tinh
        self.ma_loai_hang = ma_loai_hang
        self.don_gia = don_gia
        self.muc_ton_toi_thieu = muc_ton_toi_thieu
        self.trang_thai = trang_thai

    def to_dict(self):
        return {
            "maSanPham": self.ma_san_pham,
            "tenSanPham": self.ten_san_pham,
            "maDonViTinh": self.ma_don_vi_tinh,
            "maLoaiHang": self.ma_loai_hang,
            "donGia": self.don_gia,
            "mucTonToiThieu": self.muc_ton_toi_thieu,
            "trangThai": self.trang_thai,
        }
