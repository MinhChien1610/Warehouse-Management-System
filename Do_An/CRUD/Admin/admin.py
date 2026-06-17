from __future__ import annotations

import os

from CRUD.Admin.nhanvien import NhanVien
from CRUD.Admin.taikhoan import TaiKhoan
from CRUD.Admin.danhmuc import DanhMuc
from CRUD.Shared.khohang import KhoHang
from CRUD.Shared.hanghoa import HangHoa
from CRUD.Shared.thongke import ThongKe


class NghiepVuAdmin(
    NhanVien,
    TaiKhoan,
    DanhMuc,
    KhoHang,
    HangHoa,
    ThongKe,
):
    """Xu ly nghiep vu cua Admin."""

    def __init__(self, thu_muc_goc=None, tai_khoan_dang_nhap=None):
        self.thu_muc_goc = thu_muc_goc
        self.thu_muc_data = os.path.join(self.thu_muc_goc, "Data")
        self.tai_khoan_dang_nhap = tai_khoan_dang_nhap or {}

        self.ten_vai_tro = "Admin"
        self.la_quyen_admin = True


AdminCRUD = NghiepVuAdmin