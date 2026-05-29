class NhatKy:
    def __init__(self, ma_nhat_ky, ma_tai_khoan, hanh_dong, doi_tuong, thoi_gian, trang_thai, ghi_chu=""):
        self.ma_nhat_ky = ma_nhat_ky
        self.ma_tai_khoan = ma_tai_khoan
        self.hanh_dong = hanh_dong
        self.doi_tuong = doi_tuong
        self.thoi_gian = thoi_gian
        self.trang_thai = trang_thai
        self.ghi_chu = ghi_chu

    def to_dict(self):
        return {
            "maNhatKy": self.ma_nhat_ky,
            "maTaiKhoan": self.ma_tai_khoan,
            "hanhDong": self.hanh_dong,
            "doiTuong": self.doi_tuong,
            "thoiGian": self.thoi_gian,
            "trangThai": self.trang_thai,
            "ghiChu": self.ghi_chu,
        }
