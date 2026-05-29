from __future__ import annotations

import os

from CRUD.NhanVienKho.khohang import KhoHang
from CRUD.NhanVienKho.hanghoa import HangHoa
from CRUD.NhanVienKho.nhatky import NhatKy
from CRUD.NhanVienKho.thongke import ThongKe


class NghiepVuNhanVienKho(
    KhoHang,
    HangHoa,
    NhatKy,
    ThongKe,
):
    """Xu ly nghiep vu cua nhan vien kho."""

    def __init__(self, thu_muc_goc=None, ma_tai_khoan=None):
        self.thu_muc_goc = thu_muc_goc or self.lay_thu_muc_goc()
        self.thu_muc_data = os.path.join(self.thu_muc_goc, "Data")
        self.ma_tai_khoan = ma_tai_khoan or self.lay_ma_tai_khoan_nhan_vien_kho()


NhanVienKhoCRUD = NghiepVuNhanVienKho
