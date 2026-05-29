class Kho:
    def __init__(self, ma_kho, ten_kho, dia_diem, so_dien_thoai):
        self.ma_kho = ma_kho
        self.ten_kho = ten_kho
        self.dia_diem = dia_diem
        self.so_dien_thoai = so_dien_thoai

    def to_dict(self):
        return {
            "maKho": self.ma_kho,
            "tenKho": self.ten_kho,
            "diaDiem": self.dia_diem,
            "soDienThoai": self.so_dien_thoai,
        }
