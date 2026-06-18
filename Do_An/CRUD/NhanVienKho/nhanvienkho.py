from __future__ import annotations

import os

from CRUD.Shared.khohang import KhoHang
from CRUD.Shared.hanghoa import HangHoa
from CRUD.Shared.thongke import ThongKe
from CRUD.NhanVienKho.nhatky import NhatKy


class NghiepVuNhanVienKho(
    KhoHang,
    HangHoa,
    ThongKe,
    NhatKy,
):
    """Xu ly nghiep vu cua nhan vien kho."""

    def __init__(self, thu_muc_goc=None, ma_tai_khoan=None):
        self.thu_muc_goc = thu_muc_goc or self.lay_thu_muc_goc()
        self.thu_muc_data = os.path.join(self.thu_muc_goc, "Data")
        self.ma_tai_khoan = ma_tai_khoan or self.lay_ma_tai_khoan_nhan_vien_kho()
        self.ten_vai_tro = "Nhân viên kho"
        self.la_quyen_admin = False


NhanVienKhoCRUD = NghiepVuNhanVienKho