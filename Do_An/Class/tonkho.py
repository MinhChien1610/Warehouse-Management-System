class TonKho:
    def __init__(self, ma_kho, ma_san_pham, so_luong_ton, ma_vi_tri=""):
        self.ma_kho = ma_kho
        self.ma_san_pham = ma_san_pham
        self.so_luong_ton = so_luong_ton
        self.ma_vi_tri = ma_vi_tri

    def to_dict(self):
        return {
            "maKho": self.ma_kho,
            "maSanPham": self.ma_san_pham,
            "soLuongTon": self.so_luong_ton,
            "maViTri": self.ma_vi_tri,
        }
