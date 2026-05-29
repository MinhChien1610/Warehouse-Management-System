from __future__ import annotations

import json
import os
from copy import deepcopy
from datetime import date, datetime
from typing import Any, Dict, List, Tuple

from Class.sanpham import SanPham


class HangHoa:
    def tao_san_pham(
        self,
        ten_san_pham: str,
        ma_loai_hang: str,
        ma_don_vi_tinh: str,
        don_gia: int,
        muc_ton_toi_thieu: int,
    ):
        self.kiem_tra_thong_tin_san_pham(
            ten_san_pham,
            ma_loai_hang,
            ma_don_vi_tinh,
            don_gia,
            muc_ton_toi_thieu,
        )

        data = self.doc_json("hang_hoa.json", {})
        danh_sach = data.setdefault("sanPham", [])

        ma_san_pham = self.tao_ma_tu_dong(danh_sach, "maSanPham", "SP")

        san_pham = SanPham(
            ma_san_pham,
            ten_san_pham,
            ma_don_vi_tinh,
            ma_loai_hang,
            self.chuyen_so_nguyen(don_gia),
            self.chuyen_so_nguyen(muc_ton_toi_thieu),
        ).to_dict()

        danh_sach.append(san_pham)
        self.ghi_json("hang_hoa.json", data)
        self.ghi_nhat_ky("Thêm sản phẩm", "Hàng hóa", "Tạo sản phẩm " + ma_san_pham)

        return san_pham

    def sua_san_pham(
        self,
        ma_san_pham: str,
        ten_san_pham: str,
        ma_loai_hang: str,
        ma_don_vi_tinh: str,
        don_gia: int,
        muc_ton_toi_thieu: int,
    ):
        self.kiem_tra_thong_tin_san_pham(
            ten_san_pham,
            ma_loai_hang,
            ma_don_vi_tinh,
            don_gia,
            muc_ton_toi_thieu,
        )

        data = self.doc_json("hang_hoa.json", {})

        for san_pham in data.get("sanPham", []):
            if san_pham.get("maSanPham") == ma_san_pham:
                san_pham["tenSanPham"] = ten_san_pham
                san_pham["maLoaiHang"] = ma_loai_hang
                san_pham["maDonViTinh"] = ma_don_vi_tinh
                san_pham["donGia"] = self.chuyen_so_nguyen(don_gia)
                san_pham["mucTonToiThieu"] = self.chuyen_so_nguyen(muc_ton_toi_thieu)

                if san_pham.get("trangThai", "") == "":
                    san_pham["trangThai"] = "Đang kinh doanh"

                self.ghi_json("hang_hoa.json", data)
                self.ghi_nhat_ky("Sửa sản phẩm", "Hàng hóa", "Cập nhật sản phẩm " + ma_san_pham)

                return san_pham

        raise ValueError("Không tìm thấy sản phẩm: " + ma_san_pham)

    def ngung_kinh_doanh_san_pham(self, ma_san_pham: str):
        data = self.doc_json("hang_hoa.json", {})

        for san_pham in data.get("sanPham", []):
            if san_pham.get("maSanPham") == ma_san_pham:
                san_pham["trangThai"] = "Ngừng kinh doanh"

                self.ghi_json("hang_hoa.json", data)
                self.ghi_nhat_ky(
                    "Ngừng kinh doanh sản phẩm",
                    "Hàng hóa",
                    "Chuyển sản phẩm " + ma_san_pham + " sang trạng thái Ngừng kinh doanh",
                )

                return san_pham

        raise ValueError("Không tìm thấy sản phẩm: " + ma_san_pham)

    # =========================
    # TỒN KHO
    # =========================
