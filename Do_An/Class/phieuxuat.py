class PhieuXuat:
    def __init__(self, ma_phieu_xuat, ma_kho, ma_khach_hang, ma_tai_khoan, ngay_xuat, tong_tien, trang_thai, chi_tiet):
        self.ma_phieu_xuat = ma_phieu_xuat
        self.ma_kho = ma_kho
        self.ma_khach_hang = ma_khach_hang
        self.ma_tai_khoan = ma_tai_khoan
        self.ngay_xuat = ngay_xuat
        self.tong_tien = tong_tien
        self.trang_thai = trang_thai
        self.chi_tiet = chi_tiet

    def to_dict(self):
        return {
            "maPhieuXuat": self.ma_phieu_xuat,
            "maKho": self.ma_kho,
            "maKhachHang": self.ma_khach_hang,
            "maTaiKhoan": self.ma_tai_khoan,
            "ngayXuat": self.ngay_xuat,
            "tongTien": self.tong_tien,
            "trangThai": self.trang_thai,
            "chiTiet": self.chi_tiet,
        }
