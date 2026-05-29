class PhieuNhap:
    def __init__(self, ma_phieu_nhap, ma_nha_san_xuat, ma_kho, ma_tai_khoan, ngay_nhap, tong_tien, trang_thai, chi_tiet):
        self.ma_phieu_nhap = ma_phieu_nhap
        self.ma_nha_san_xuat = ma_nha_san_xuat
        self.ma_kho = ma_kho
        self.ma_tai_khoan = ma_tai_khoan
        self.ngay_nhap = ngay_nhap
        self.tong_tien = tong_tien
        self.trang_thai = trang_thai
        self.chi_tiet = chi_tiet

    def to_dict(self):
        return {
            "maPhieuNhap": self.ma_phieu_nhap,
            "maNhaSanXuat": self.ma_nha_san_xuat,
            "maKho": self.ma_kho,
            "maTaiKhoan": self.ma_tai_khoan,
            "ngayNhap": self.ngay_nhap,
            "tongTien": self.tong_tien,
            "trangThai": self.trang_thai,
            "chiTiet": self.chi_tiet,
        }
