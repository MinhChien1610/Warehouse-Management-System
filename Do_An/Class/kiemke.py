class KiemKe:
    def __init__(self, ma_kiem_ke, ma_kho, ngay_kiem_ke, ghi_chu, chi_tiet):
        self.ma_kiem_ke = ma_kiem_ke
        self.ma_kho = ma_kho
        self.ngay_kiem_ke = ngay_kiem_ke
        self.ghi_chu = ghi_chu
        self.chi_tiet = chi_tiet

    def to_dict(self):
        return {
            "maKiemKe": self.ma_kiem_ke,
            "maKho": self.ma_kho,
            "ngayKiemKe": self.ngay_kiem_ke,
            "ghiChu": self.ghi_chu,
            "chiTiet": self.chi_tiet,
        }
