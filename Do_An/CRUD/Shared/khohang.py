import json
import os
from copy import deepcopy
from datetime import date, datetime

from Class.tonkho import TonKho
from Class.phieunhap import PhieuNhap
from Class.phieuxuat import PhieuXuat
from Class.kiemke import KiemKe
from Calculator.phieu import tinh_tong_tien_chi_tiet
from Calculator.common import chuyen_so_nguyen
from Calculator.tonkho import lay_canh_bao_ton_thap as tinh_canh_bao_ton_thap
from Calculator.tonkho import lap_du_lieu_ton_kho

class KhoHang:
    # =========================
    # FILE JSON
    # =========================
    def lay_thu_muc_goc(self):
        thu_muc = os.path.dirname(os.path.abspath(__file__))

        while True:
            if os.path.exists(os.path.join(thu_muc, "Data")):
                return thu_muc

            thu_muc_cha = os.path.dirname(thu_muc)

            if thu_muc_cha == thu_muc:
                return os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(os.path.abspath(__file__))
                    )
                )

            thu_muc = thu_muc_cha

    def lay_duong_dan_file(self, ten_file):
        return os.path.join(self.thu_muc_data, ten_file)

    def doc_json(self, ten_file, mac_dinh):
        duong_dan = self.lay_duong_dan_file(ten_file)

        if not os.path.exists(duong_dan):
            return deepcopy(mac_dinh)

        for encoding in ["utf-8-sig", "utf-8", "cp1258"]:
            try:
                with open(duong_dan, "r", encoding=encoding) as file:
                    return json.load(file)
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue

        return deepcopy(mac_dinh)

    def ghi_json(self, ten_file, data):
        duong_dan = self.lay_duong_dan_file(ten_file)

        with open(duong_dan, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    # =========================
    # ĐỊNH DẠNG
    # =========================
    def dinh_dang_tien_hien_thi(self, value):
        so = self.chuyen_so_nguyen(value)
        return f"{so:,}".replace(",", ".")

    def dinh_dang_chenh_lech(self, chenh_lech):
        chenh_lech = int(chenh_lech)

        if chenh_lech < 0:
            return "Thiếu " + str(abs(chenh_lech))

        if chenh_lech > 0:
            return "Dư " + str(chenh_lech)

        return "Đủ"

    def them_hien_thi_tien_vao_phieu(self, phieu):
        phieu["tongTienHienThi"] = self.dinh_dang_tien_hien_thi(phieu.get("tongTien", 0))

        for item in phieu.get("chiTiet", []):
            item["donGiaHienThi"] = self.dinh_dang_tien_hien_thi(item.get("donGia", 0))
            item["thanhTienHienThi"] = self.dinh_dang_tien_hien_thi(
                self.chuyen_so_nguyen(item.get("soLuong", 0))
                * self.chuyen_so_nguyen(item.get("donGia", 0))
            )

        return phieu

    def la_admin(self):
        return getattr(self, "la_quyen_admin", False)

    # =========================
    # TÀI KHOẢN / PHÂN QUYỀN KHO
    # =========================
    def lay_ma_tai_khoan_nhan_vien_kho(self):
        data = self.doc_json("nguoi_dung.json", {})

        vai_tro_map = {}

        for vai_tro in data.get("vaiTro", []):
            ma_vai_tro = vai_tro.get("maVaiTro", "")
            ten_vai_tro = vai_tro.get("tenVaiTro", "")
            vai_tro_map[ma_vai_tro] = ten_vai_tro

        for phan_quyen in data.get("phanQuyen", []):
            ma_vai_tro = phan_quyen.get("maVaiTro", "")
            ten_vai_tro = vai_tro_map.get(ma_vai_tro, "")

            if ten_vai_tro in ["NhanVienKho", "Nhân viên kho"]:
                return phan_quyen.get("maTaiKhoan", "")

        return ""

    def lay_danh_sach_ma_kho_duoc_phan_cong(self):
        data = self.doc_json("nguoi_dung.json", {})
        danh_sach = []

        for phan_cong in data.get("phanCongKho", []):
            dung_tai_khoan = phan_cong.get("maTaiKhoan") == self.ma_tai_khoan
            dang_hoat_dong = phan_cong.get("trangThai") is True

            if dung_tai_khoan and dang_hoat_dong:
                ma_kho = phan_cong.get("maKho", "")

                if ma_kho != "" and ma_kho not in danh_sach:
                    danh_sach.append(ma_kho)

        return danh_sach

    def kiem_tra_kho_duoc_phan_cong(self, ma_kho):
        if self.la_admin():
            return

        danh_sach_ma_kho = self.lay_danh_sach_ma_kho_duoc_phan_cong()

        if len(danh_sach_ma_kho) == 0:
            raise ValueError("Tài khoản này chưa được phân công kho.")

        if ma_kho not in danh_sach_ma_kho:
            raise ValueError("Bạn không được thao tác trên kho " + str(ma_kho) + ".")

    def loc_theo_kho_duoc_phan_cong(self, danh_sach, truong_kho="maKho"):
        if self.la_admin():
            return danh_sach

        danh_sach_ma_kho = self.lay_danh_sach_ma_kho_duoc_phan_cong()

        if len(danh_sach_ma_kho) == 0:
            return []

        ket_qua = []

        for item in danh_sach:
            if item.get(truong_kho, "") in danh_sach_ma_kho:
                ket_qua.append(item)

        return ket_qua

    # =========================
    # DANH MỤC
    # =========================
    def lay_danh_sach_kho(self):
        data = self.doc_json("kho_hang.json", {})
        return self.loc_theo_kho_duoc_phan_cong(data.get("kho", []))

    def lay_danh_sach_vi_tri(self, ma_kho=""):
        data = self.doc_json("kho_hang.json", {})
        danh_sach = data.get("viTriKho", [])

        if ma_kho == "":
            return self.loc_theo_kho_duoc_phan_cong(danh_sach)

        self.kiem_tra_kho_duoc_phan_cong(ma_kho)

        return [
            item
            for item in danh_sach
            if item.get("maKho") == ma_kho
        ]

    def lay_danh_sach_san_pham(self):
        data = self.doc_json("hang_hoa.json", {})
        return data.get("sanPham", [])

    def lay_danh_sach_nha_san_xuat(self):
        data = self.doc_json("doi_tac.json", {})
        return data.get("nhaSanXuat", [])

    def lay_danh_sach_khach_hang(self):
        data = self.doc_json("doi_tac.json", {})
        return data.get("khachHang", [])

    def tim_kho(self, ma_kho):
        for kho in self.lay_danh_sach_kho():
            if kho.get("maKho") == ma_kho:
                return kho

        return None

    def tim_san_pham(self, ma_san_pham):
        for san_pham in self.lay_danh_sach_san_pham():
            if san_pham.get("maSanPham") == ma_san_pham:
                return san_pham

        return None

    def la_san_pham_dang_kinh_doanh(self, san_pham):
        trang_thai = str(san_pham.get("trangThai", "")).strip().lower()
        return trang_thai not in [
            "ngừng kinh doanh",
            "ngung kinh doanh",
            "đã ngừng",
            "da ngung",
            "false",
            "0",
            "inactive",
        ]

    # =========================
    # TỒN KHO
    # =========================
    def lay_ton_kho(self):
        kho_data = self.doc_json("kho_hang.json", {})
        hang_data = self.doc_json("hang_hoa.json", {})

        ket_qua = lap_du_lieu_ton_kho(
            self.loc_theo_kho_duoc_phan_cong(kho_data.get("tonKho", [])),
            hang_data.get("sanPham", []),
            self.loc_theo_kho_duoc_phan_cong(kho_data.get("viTriKho", [])),
        )

        for ton in ket_qua:
            ton["maViTri"] = ton.get("viTriHang", "")
            ton["donGiaHienThi"] = self.dinh_dang_tien_hien_thi(ton.get("donGia", 0))

        return ket_qua

    def lay_so_luong_ton(self, ma_kho, ma_san_pham):
        self.kiem_tra_kho_duoc_phan_cong(ma_kho)

        kho_data = self.doc_json("kho_hang.json", {})

        for ton in kho_data.get("tonKho", []):
            dung_kho = ton.get("maKho") == ma_kho
            dung_san_pham = ton.get("maSanPham") == ma_san_pham

            if dung_kho and dung_san_pham:
                return self.chuyen_so_nguyen(ton.get("soLuongTon", 0))

        return 0

    def cap_nhat_ton_kho(
        self,
        ma_kho,
        ma_san_pham,
        so_luong_thay_doi,
        ma_vi_tri="",
        cho_phep_am=False,
    ):
        self.kiem_tra_kho_duoc_phan_cong(ma_kho)

        so_luong_thay_doi = self.chuyen_so_nguyen(so_luong_thay_doi)

        kho_data = self.doc_json("kho_hang.json", {})
        danh_sach_ton = kho_data.setdefault("tonKho", [])

        for ton in danh_sach_ton:
            dung_kho = ton.get("maKho") == ma_kho
            dung_san_pham = ton.get("maSanPham") == ma_san_pham

            if dung_kho and dung_san_pham:
                so_luong_cu = self.chuyen_so_nguyen(ton.get("soLuongTon", 0))
                so_luong_moi = so_luong_cu + so_luong_thay_doi

                if so_luong_moi < 0 and not cho_phep_am:
                    raise ValueError("Số lượng tồn kho không đủ.")

                ton["soLuongTon"] = so_luong_moi

                if ma_vi_tri != "":
                    ton["maViTri"] = ma_vi_tri

                self.ghi_json("kho_hang.json", kho_data)
                return

        if so_luong_thay_doi < 0 and not cho_phep_am:
            raise ValueError("Sản phẩm chưa có tồn kho nên không thể xuất hàng.")

        danh_sach_ton.append(
            TonKho(ma_kho, ma_san_pham, so_luong_thay_doi, ma_vi_tri).to_dict()
        )

        self.ghi_json("kho_hang.json", kho_data)

    def dat_lai_ton_kho(self, ma_kho, ma_san_pham, so_luong_moi):
        self.kiem_tra_kho_duoc_phan_cong(ma_kho)

        so_luong_moi = self.chuyen_so_nguyen(so_luong_moi)

        if so_luong_moi < 0:
            raise ValueError("Số lượng tồn mới không hợp lệ.")

        kho_data = self.doc_json("kho_hang.json", {})
        danh_sach_ton = kho_data.setdefault("tonKho", [])

        for ton in danh_sach_ton:
            dung_kho = ton.get("maKho") == ma_kho
            dung_san_pham = ton.get("maSanPham") == ma_san_pham

            if dung_kho and dung_san_pham:
                ton["soLuongTon"] = so_luong_moi
                self.ghi_json("kho_hang.json", kho_data)
                return

        danh_sach_ton.append(
            TonKho(ma_kho, ma_san_pham, so_luong_moi).to_dict()
        )

        self.ghi_json("kho_hang.json", kho_data)

    def lay_canh_bao_ton_thap(self):
        kho_data = self.doc_json("kho_hang.json", {})
        hang_data = self.doc_json("hang_hoa.json", {})

        ket_qua = tinh_canh_bao_ton_thap(
            self.loc_theo_kho_duoc_phan_cong(kho_data.get("tonKho", [])),
            hang_data.get("sanPham", []),
            self.loc_theo_kho_duoc_phan_cong(kho_data.get("viTriKho", [])),
        )

        for ton in ket_qua:
            ton["maViTri"] = ton.get("viTriHang", "")

        return ket_qua

    # =========================
    # PHIẾU NHẬP
    # =========================
    def tao_phieu_nhap(
        self,
        ma_nha_san_xuat,
        ma_kho,
        chi_tiet,
        ngay_nhap=None,
        luu_tam=False,
    ):
        self.kiem_tra_kho_ton_tai(ma_kho)
        self.kiem_tra_chi_tiet_hang(chi_tiet)

        data = self.doc_json("phieu_nhap.json", [])
        ma_phieu = self.tao_ma_tu_dong(data, "maPhieuNhap", "PN")
        chi_tiet_chuan = self.chuan_hoa_chi_tiet(chi_tiet)

        phieu = PhieuNhap(
            ma_phieu,
            ma_nha_san_xuat,
            ma_kho,
            self.ma_tai_khoan,
            ngay_nhap or self.lay_ngay_hien_tai(),
            self.tinh_tong_tien(chi_tiet_chuan),
            "Lưu tạm" if luu_tam else "Đã nhập",
            chi_tiet_chuan,
        ).to_dict()

        self.them_hien_thi_tien_vao_phieu(phieu)

        data.append(phieu)
        self.ghi_json("phieu_nhap.json", data)

        if not luu_tam:
            self.cap_nhat_ton_theo_phieu_nhap(phieu)

        hanh_dong = "Lưu tạm phiếu nhập" if luu_tam else "Thêm phiếu nhập"
        self.ghi_nhat_ky(hanh_dong, "Phiếu nhập", hanh_dong + " " + ma_phieu)

        return phieu

    def cap_nhat_phieu_nhap(
        self,
        ma_phieu_nhap,
        ma_nha_san_xuat,
        ma_kho,
        chi_tiet,
        luu_tam=False,
    ):
        data = self.doc_json("phieu_nhap.json", [])
        phieu = self.tim_phieu(data, "maPhieuNhap", ma_phieu_nhap)

        if not self.la_phieu_luu_tam(phieu):
            raise ValueError("Chỉ được sửa phiếu nhập đang lưu tạm.")

        self.kiem_tra_kho_ton_tai(ma_kho)
        self.kiem_tra_chi_tiet_hang(chi_tiet)
        self.kiem_tra_chi_duoc_sua_so_luong_phieu_nhap(phieu, ma_nha_san_xuat, ma_kho, chi_tiet)

        chi_tiet_chuan = self.chuan_hoa_chi_tiet(chi_tiet)

        phieu["tongTien"] = self.tinh_tong_tien(chi_tiet_chuan)
        phieu["trangThai"] = "Lưu tạm" if luu_tam else "Đã nhập"
        phieu["chiTiet"] = chi_tiet_chuan

        self.them_hien_thi_tien_vao_phieu(phieu)
        self.ghi_json("phieu_nhap.json", data)

        if not luu_tam:
            self.cap_nhat_ton_theo_phieu_nhap(phieu)

        hanh_dong = "Cập nhật phiếu nhập tạm" if luu_tam else "Xác nhận phiếu nhập"
        self.ghi_nhat_ky(hanh_dong, "Phiếu nhập", hanh_dong + " " + ma_phieu_nhap)

        return phieu

    def xoa_phieu_nhap(self, ma_phieu_nhap):
        data = self.doc_json("phieu_nhap.json", [])
        phieu, con_lai = self.tach_phieu(data, "maPhieuNhap", ma_phieu_nhap)

        self.kiem_tra_kho_duoc_phan_cong(phieu.get("maKho", ""))

        if self.la_phieu_luu_tam(phieu):
            self.ghi_json("phieu_nhap.json", con_lai)
            self.ghi_nhat_ky(
                "Xóa phiếu nhập tạm",
                "Phiếu nhập",
                "Xóa phiếu nhập tạm " + ma_phieu_nhap,
            )
            return phieu

        if not self.la_admin():
            raise ValueError("Nhân viên kho chỉ được xóa phiếu nhập lưu tạm.")

        return self.huy_phieu_nhap_admin(ma_phieu_nhap)

    def cap_nhat_ton_theo_phieu_nhap(self, phieu):
        self.kiem_tra_kho_duoc_phan_cong(phieu.get("maKho", ""))

        for item in phieu.get("chiTiet", []):
            self.cap_nhat_ton_kho(
                phieu.get("maKho", ""),
                item.get("maSanPham", ""),
                self.chuyen_so_nguyen(item.get("soLuong", 0)),
                item.get("maViTri", ""),
            )

    # =========================
    # PHIẾU XUẤT
    # =========================
    def tao_phieu_xuat(
        self,
        ma_khach_hang,
        ma_kho,
        chi_tiet,
        ngay_xuat=None,
        luu_tam=False,
    ):
        self.kiem_tra_kho_ton_tai(ma_kho)
        self.kiem_tra_chi_tiet_hang(chi_tiet)

        chi_tiet_chuan = self.chuan_hoa_chi_tiet(chi_tiet)

        if not luu_tam:
            self.kiem_tra_du_ton_khi_xuat(ma_kho, chi_tiet_chuan)

        data = self.doc_json("phieu_xuat.json", [])
        ma_phieu = self.tao_ma_tu_dong(data, "maPhieuXuat", "PX")

        phieu = PhieuXuat(
            ma_phieu,
            ma_kho,
            ma_khach_hang,
            self.ma_tai_khoan,
            ngay_xuat or self.lay_ngay_hien_tai(),
            self.tinh_tong_tien(chi_tiet_chuan),
            "Lưu tạm" if luu_tam else "Đã xuất",
            chi_tiet_chuan,
        ).to_dict()

        self.them_hien_thi_tien_vao_phieu(phieu)

        data.append(phieu)
        self.ghi_json("phieu_xuat.json", data)

        if not luu_tam:
            self.cap_nhat_ton_theo_phieu_xuat(phieu)

        hanh_dong = "Lưu tạm phiếu xuất" if luu_tam else "Thêm phiếu xuất"
        self.ghi_nhat_ky(hanh_dong, "Phiếu xuất", hanh_dong + " " + ma_phieu)

        return phieu

    def cap_nhat_phieu_xuat(
        self,
        ma_phieu_xuat,
        ma_khach_hang,
        ma_kho,
        chi_tiet,
        luu_tam=False,
    ):
        data = self.doc_json("phieu_xuat.json", [])
        phieu = self.tim_phieu(data, "maPhieuXuat", ma_phieu_xuat)

        if not self.la_phieu_luu_tam(phieu):
            raise ValueError("Chỉ được sửa phiếu xuất đang lưu tạm.")

        self.kiem_tra_kho_ton_tai(ma_kho)
        self.kiem_tra_chi_tiet_hang(chi_tiet)
        self.kiem_tra_chi_duoc_sua_so_luong_phieu_xuat(phieu, ma_khach_hang, ma_kho, chi_tiet)

        chi_tiet_chuan = self.chuan_hoa_chi_tiet(chi_tiet)

        if not luu_tam:
            self.kiem_tra_du_ton_khi_xuat(ma_kho, chi_tiet_chuan)

        phieu["tongTien"] = self.tinh_tong_tien(chi_tiet_chuan)
        phieu["trangThai"] = "Lưu tạm" if luu_tam else "Đã xuất"
        phieu["chiTiet"] = chi_tiet_chuan

        self.them_hien_thi_tien_vao_phieu(phieu)
        self.ghi_json("phieu_xuat.json", data)

        if not luu_tam:
            self.cap_nhat_ton_theo_phieu_xuat(phieu)

        hanh_dong = "Cập nhật phiếu xuất tạm" if luu_tam else "Xác nhận phiếu xuất"
        self.ghi_nhat_ky(hanh_dong, "Phiếu xuất", hanh_dong + " " + ma_phieu_xuat)

        return phieu

    def xoa_phieu_xuat(self, ma_phieu_xuat):
        data = self.doc_json("phieu_xuat.json", [])
        phieu, con_lai = self.tach_phieu(data, "maPhieuXuat", ma_phieu_xuat)

        self.kiem_tra_kho_duoc_phan_cong(phieu.get("maKho", ""))

        if self.la_phieu_luu_tam(phieu):
            self.ghi_json("phieu_xuat.json", con_lai)
            self.ghi_nhat_ky(
                "Xóa phiếu xuất tạm",
                "Phiếu xuất",
                "Xóa phiếu xuất tạm " + ma_phieu_xuat,
            )
            return phieu

        if not self.la_admin():
            raise ValueError("Nhân viên kho chỉ được xóa phiếu xuất lưu tạm.")

        return self.huy_phieu_xuat_admin(ma_phieu_xuat)

    def kiem_tra_du_ton_khi_xuat(self, ma_kho, chi_tiet):
        self.kiem_tra_kho_duoc_phan_cong(ma_kho)

        for item in chi_tiet:
            ma_san_pham = item.get("maSanPham", "")
            so_luong = self.chuyen_so_nguyen(item.get("soLuong", 0))
            so_luong_ton = self.lay_so_luong_ton(ma_kho, ma_san_pham)

            if so_luong_ton < so_luong:
                raise ValueError("Không đủ tồn kho để xuất sản phẩm " + ma_san_pham + ".")

    def cap_nhat_ton_theo_phieu_xuat(self, phieu):
        self.kiem_tra_kho_duoc_phan_cong(phieu.get("maKho", ""))

        for item in phieu.get("chiTiet", []):
            self.cap_nhat_ton_kho(
                phieu.get("maKho", ""),
                item.get("maSanPham", ""),
                -self.chuyen_so_nguyen(item.get("soLuong", 0)),
            )

    # =========================
    # KIỂM KÊ
    # =========================
    def tao_phieu_kiem_ke(
        self,
        ma_kho,
        chi_tiet,
        ghi_chu="",
        ngay_kiem_ke=None,
        luu_tam=False,
    ):
        self.kiem_tra_kho_ton_tai(ma_kho)

        if len(chi_tiet) == 0:
            raise ValueError("Chi tiết kiểm kê không được rỗng.")

        chi_tiet_chuan = self.chuan_hoa_chi_tiet_kiem_ke(ma_kho, chi_tiet)

        data = self.doc_json("kiem_ke.json", [])
        ma_phieu = self.tao_ma_tu_dong(data, "maKiemKe", "KK")

        phieu = KiemKe(
            ma_phieu,
            ma_kho,
            ngay_kiem_ke or self.lay_ngay_hien_tai(),
            ghi_chu,
            chi_tiet_chuan,
        ).to_dict()
        phieu["trangThai"] = "Lưu tạm" if luu_tam else "Đã kiểm kê"

        data.append(phieu)
        self.ghi_json("kiem_ke.json", data)

        if not luu_tam:
            for item in chi_tiet_chuan:
                self.dat_lai_ton_kho(
                    ma_kho,
                    item.get("maSanPham", ""),
                    self.chuyen_so_nguyen(item.get("soLuongThucTe", 0)),
                )

        hanh_dong = "Lưu tạm kiểm kê" if luu_tam else "Kiểm kê kho"
        self.ghi_nhat_ky(hanh_dong, "Kiểm kê", "Tạo phiếu kiểm kê " + ma_phieu)

        return phieu

    def cap_nhat_phieu_kiem_ke(
        self,
        ma_kiem_ke,
        ma_kho,
        chi_tiet,
        ghi_chu="",
        luu_tam=False,
    ):
        data = self.doc_json("kiem_ke.json", [])
        phieu = self.tim_phieu(data, "maKiemKe", ma_kiem_ke)

        if not self.la_phieu_luu_tam(phieu):
            raise ValueError("Chỉ được sửa phiếu kiểm kê đang lưu tạm.")

        self.kiem_tra_kho_ton_tai(ma_kho)
        self.kiem_tra_chi_duoc_sua_so_luong_kiem_ke(phieu, ma_kho, chi_tiet)

        chi_tiet_chuan = self.chuan_hoa_chi_tiet_kiem_ke(ma_kho, chi_tiet)

        phieu["ghiChu"] = ghi_chu
        phieu["trangThai"] = "Lưu tạm" if luu_tam else "Đã kiểm kê"
        phieu["chiTiet"] = chi_tiet_chuan

        self.ghi_json("kiem_ke.json", data)

        if not luu_tam:
            for item in chi_tiet_chuan:
                self.dat_lai_ton_kho(
                    ma_kho,
                    item.get("maSanPham", ""),
                    self.chuyen_so_nguyen(item.get("soLuongThucTe", 0)),
                )

        hanh_dong = "Cập nhật kiểm kê tạm" if luu_tam else "Xác nhận kiểm kê"
        self.ghi_nhat_ky(hanh_dong, "Kiểm kê", hanh_dong + " " + ma_kiem_ke)

        return phieu

    def xoa_phieu_kiem_ke(self, ma_kiem_ke, khoi_phuc_ton_cu=True):
        data = self.doc_json("kiem_ke.json", [])
        phieu, con_lai = self.tach_phieu(data, "maKiemKe", ma_kiem_ke)

        self.kiem_tra_kho_duoc_phan_cong(phieu.get("maKho", ""))

        if self.la_phieu_luu_tam(phieu):
            self.ghi_json("kiem_ke.json", con_lai)
            self.ghi_nhat_ky("Xóa phiếu kiểm kê tạm", "Kiểm kê", "Xóa phiếu kiểm kê tạm " + ma_kiem_ke)
            return phieu

        if not self.la_admin():
            raise ValueError("Nhân viên kho chỉ được xóa phiếu kiểm kê lưu tạm.")

        return self.huy_phieu_kiem_ke_admin(ma_kiem_ke, khoi_phuc_ton_cu)

    # =========================
    # HỦY PHIẾU DÀNH CHO ADMIN
    # =========================
    def huy_phieu_nhap_admin(self, ma_phieu_nhap):
        if not self.la_admin():
            raise ValueError("Chỉ admin mới được hủy phiếu nhập đã chốt.")

        data = self.doc_json("phieu_nhap.json", [])
        phieu = self.tim_phieu(data, "maPhieuNhap", ma_phieu_nhap)

        if phieu.get("trangThai") == "Đã hủy":
            raise ValueError("Phiếu nhập này đã hủy rồi.")

        if self.la_phieu_luu_tam(phieu):
            phieu, con_lai = self.tach_phieu(data, "maPhieuNhap", ma_phieu_nhap)
            self.ghi_json("phieu_nhap.json", con_lai)
            return phieu

        for item in phieu.get("chiTiet", []):
            self.cap_nhat_ton_kho(
                phieu.get("maKho", ""),
                item.get("maSanPham", ""),
                -self.chuyen_so_nguyen(item.get("soLuong", 0)),
                item.get("maViTri", ""),
                cho_phep_am=True,
            )

        phieu["trangThai"] = "Đã hủy"
        self.ghi_json("phieu_nhap.json", data)
        self.ghi_nhat_ky("Hủy phiếu nhập", "Phiếu nhập", "Hủy phiếu nhập " + ma_phieu_nhap)

        return phieu

    def huy_phieu_xuat_admin(self, ma_phieu_xuat):
        if not self.la_admin():
            raise ValueError("Chỉ admin mới được hủy phiếu xuất đã chốt.")

        data = self.doc_json("phieu_xuat.json", [])
        phieu = self.tim_phieu(data, "maPhieuXuat", ma_phieu_xuat)

        if phieu.get("trangThai") == "Đã hủy":
            raise ValueError("Phiếu xuất này đã hủy rồi.")

        if self.la_phieu_luu_tam(phieu):
            phieu, con_lai = self.tach_phieu(data, "maPhieuXuat", ma_phieu_xuat)
            self.ghi_json("phieu_xuat.json", con_lai)
            return phieu

        for item in phieu.get("chiTiet", []):
            self.cap_nhat_ton_kho(
                phieu.get("maKho", ""),
                item.get("maSanPham", ""),
                self.chuyen_so_nguyen(item.get("soLuong", 0)),
            )

        phieu["trangThai"] = "Đã hủy"
        self.ghi_json("phieu_xuat.json", data)
        self.ghi_nhat_ky("Hủy phiếu xuất", "Phiếu xuất", "Hủy phiếu xuất " + ma_phieu_xuat)

        return phieu

    def huy_phieu_kiem_ke_admin(self, ma_kiem_ke, khoi_phuc_ton_cu=True):
        if not self.la_admin():
            raise ValueError("Chỉ admin mới được hủy phiếu kiểm kê đã chốt.")

        data = self.doc_json("kiem_ke.json", [])
        phieu = self.tim_phieu(data, "maKiemKe", ma_kiem_ke)

        if phieu.get("trangThai") == "Đã hủy":
            raise ValueError("Phiếu kiểm kê này đã hủy rồi.")

        if self.la_phieu_luu_tam(phieu):
            phieu, con_lai = self.tach_phieu(data, "maKiemKe", ma_kiem_ke)
            self.ghi_json("kiem_ke.json", con_lai)
            return phieu

        if khoi_phuc_ton_cu:
            for item in phieu.get("chiTiet", []):
                self.dat_lai_ton_kho(
                    phieu.get("maKho", ""),
                    item.get("maSanPham", ""),
                    self.chuyen_so_nguyen(item.get("soLuongHeThong", 0)),
                )

        phieu["trangThai"] = "Đã hủy"
        self.ghi_json("kiem_ke.json", data)
        self.ghi_nhat_ky("Hủy phiếu kiểm kê", "Kiểm kê", "Hủy phiếu kiểm kê " + ma_kiem_ke)

        return phieu

    # =========================
    # KIỂM TRA DỮ LIỆU
    # =========================
    def kiem_tra_kho_ton_tai(self, ma_kho):
        self.kiem_tra_kho_duoc_phan_cong(ma_kho)

        if self.tim_kho(ma_kho) is None:
            raise ValueError("Mã kho không tồn tại hoặc bạn không có quyền thao tác: " + ma_kho)

    def kiem_tra_san_pham_ton_tai(self, ma_san_pham):
        san_pham = self.tim_san_pham(ma_san_pham)

        if san_pham is None:
            raise ValueError("Mã sản phẩm không tồn tại: " + ma_san_pham)

        return san_pham

    def kiem_tra_chi_tiet_hang(self, chi_tiet):
        if len(chi_tiet) == 0:
            raise ValueError("Chi tiết phiếu không được rỗng.")

        for item in chi_tiet:
            ma_san_pham = str(item.get("maSanPham", "")).strip()
            so_luong = self.chuyen_so_nguyen(item.get("soLuong", 0))
            don_gia = self.chuyen_so_nguyen(item.get("donGia", 0))

            if ma_san_pham == "":
                raise ValueError("Mã sản phẩm không được rỗng.")

            if so_luong <= 0:
                raise ValueError("Số lượng phải lớn hơn 0.")

            if don_gia <= 0:
                raise ValueError("Đơn giá phải lớn hơn 0.")

            san_pham = self.kiem_tra_san_pham_ton_tai(ma_san_pham)

            if not self.la_san_pham_dang_kinh_doanh(san_pham):
                raise ValueError("Sản phẩm " + ma_san_pham + " đã ngừng kinh doanh, không thể chọn vào phiếu.")

    def kiem_tra_chi_duoc_sua_so_luong_phieu_nhap(self, phieu, ma_nha_san_xuat, ma_kho, chi_tiet_moi):
        if phieu.get("maNhaSanXuat", "") != ma_nha_san_xuat:
            raise ValueError("Không được sửa nhà sản xuất của phiếu.")

        if phieu.get("maKho", "") != ma_kho:
            raise ValueError("Không được sửa kho của phiếu.")

        self.kiem_tra_chi_duoc_sua_so_luong_chi_tiet(
            phieu.get("chiTiet", []),
            chi_tiet_moi,
            bat_buoc_giong_vi_tri=True,
        )

    def kiem_tra_chi_duoc_sua_so_luong_phieu_xuat(self, phieu, ma_khach_hang, ma_kho, chi_tiet_moi):
        if phieu.get("maKhachHang", "") != ma_khach_hang:
            raise ValueError("Không được sửa khách hàng của phiếu.")

        if phieu.get("maKho", "") != ma_kho:
            raise ValueError("Không được sửa kho của phiếu.")

        self.kiem_tra_chi_duoc_sua_so_luong_chi_tiet(
            phieu.get("chiTiet", []),
            chi_tiet_moi,
            bat_buoc_giong_vi_tri=False,
        )

    def kiem_tra_chi_duoc_sua_so_luong_kiem_ke(self, phieu, ma_kho, chi_tiet_moi):
        if phieu.get("maKho", "") != ma_kho:
            raise ValueError("Không được sửa kho của phiếu kiểm kê.")

        cu = phieu.get("chiTiet", [])
        cu_map = {}

        for item in cu:
            cu_map[item.get("maSanPham", "")] = item

        moi_map = {}

        for item in chi_tiet_moi:
            moi_map[item.get("maSanPham", "")] = item

        if set(cu_map.keys()) != set(moi_map.keys()):
            raise ValueError("Không được thêm, xóa hoặc đổi mã sản phẩm trong phiếu kiểm kê.")

    def kiem_tra_chi_duoc_sua_so_luong_chi_tiet(self, chi_tiet_cu, chi_tiet_moi, bat_buoc_giong_vi_tri):
        cu_map = {}
        moi_map = {}

        for item in chi_tiet_cu:
            ma_san_pham = item.get("maSanPham", "")
            cu_map[ma_san_pham] = item

        for item in chi_tiet_moi:
            ma_san_pham = item.get("maSanPham", "")
            moi_map[ma_san_pham] = item

        if set(cu_map.keys()) != set(moi_map.keys()):
            raise ValueError("Không được thêm, xóa hoặc đổi mã sản phẩm trong phiếu.")

        for ma_san_pham, item_cu in cu_map.items():
            item_moi = moi_map[ma_san_pham]

            if self.chuyen_so_nguyen(item_cu.get("donGia", 0)) != self.chuyen_so_nguyen(item_moi.get("donGia", 0)):
                raise ValueError("Không được sửa đơn giá sản phẩm " + ma_san_pham + ".")

            if bat_buoc_giong_vi_tri:
                vi_tri_cu = item_cu.get("maViTri", "")
                vi_tri_moi = item_moi.get("maViTri", "")

                if vi_tri_cu != vi_tri_moi:
                    raise ValueError("Không được sửa vị trí sản phẩm " + ma_san_pham + ".")

    # =========================
    # CHUẨN HÓA DỮ LIỆU
    # =========================
    def chuan_hoa_chi_tiet(self, chi_tiet):
        ket_qua_map = {}

        for item in chi_tiet:
            ma_san_pham = str(item.get("maSanPham", "")).strip()
            so_luong = self.chuyen_so_nguyen(item.get("soLuong", 0))
            don_gia = self.chuyen_so_nguyen(item.get("donGia", 0))

            if so_luong <= 0:
                raise ValueError("Số lượng sản phẩm " + ma_san_pham + " phải lớn hơn 0.")

            if don_gia <= 0:
                raise ValueError("Đơn giá sản phẩm " + ma_san_pham + " phải lớn hơn 0.")

            if ma_san_pham in ket_qua_map:
                ket_qua_map[ma_san_pham]["soLuong"] += so_luong
                continue

            dong = {
                "maSanPham": ma_san_pham,
                "soLuong": so_luong,
                "donGia": don_gia,
                "donGiaHienThi": self.dinh_dang_tien_hien_thi(don_gia),
                "thanhTienHienThi": self.dinh_dang_tien_hien_thi(so_luong * don_gia),
            }

            if item.get("maViTri", "") != "":
                dong["maViTri"] = item.get("maViTri", "")

            ket_qua_map[ma_san_pham] = dong

        return list(ket_qua_map.values())

    def chuan_hoa_chi_tiet_kiem_ke(self, ma_kho, chi_tiet):
        self.kiem_tra_kho_duoc_phan_cong(ma_kho)

        ket_qua = []
        san_pham_da_chon = set()

        for item in chi_tiet:
            ma_san_pham = str(item.get("maSanPham", "")).strip()

            if ma_san_pham == "":
                raise ValueError("Vui lòng chọn sản phẩm kiểm kê.")

            so_luong_thuc_te = self.chuyen_so_nguyen(item.get("soLuongThucTe", 0))

            if so_luong_thuc_te < 0:
                raise ValueError("Số lượng thực tế không được âm.")

            if ma_san_pham in san_pham_da_chon:
                raise ValueError("Sản phẩm " + ma_san_pham + " bị trùng trong phiếu kiểm kê.")

            san_pham_da_chon.add(ma_san_pham)
            self.kiem_tra_san_pham_ton_tai(ma_san_pham)

            so_luong_he_thong = self.lay_so_luong_ton(ma_kho, ma_san_pham)
            chenh_lech = so_luong_thuc_te - so_luong_he_thong

            ket_qua.append({
                "maSanPham": ma_san_pham,
                "soLuongHeThong": so_luong_he_thong,
                "soLuongThucTe": so_luong_thuc_te,
                "chenhLech": chenh_lech,
                "chenhLechHienThi": self.dinh_dang_chenh_lech(chenh_lech),
                "soLuongChenhLechHienThi": abs(chenh_lech),
            })

        return ket_qua

    # =========================
    # HÀM PHỤ
    # =========================
    def tinh_tong_tien(self, chi_tiet):
        return tinh_tong_tien_chi_tiet(chi_tiet)

    def tim_phieu(self, danh_sach, truong_ma, ma_phieu):
        for phieu in danh_sach:
            if phieu.get(truong_ma) == ma_phieu:
                self.kiem_tra_kho_duoc_phan_cong(phieu.get("maKho", ""))
                return phieu

        raise ValueError("Không tìm thấy phiếu: " + ma_phieu)

    def tach_phieu(
        self,
        danh_sach,
        truong_ma,
        ma_phieu,
    ):
        phieu_can_xoa = None
        danh_sach_con_lai = []

        for phieu in danh_sach:
            if phieu.get(truong_ma) == ma_phieu:
                phieu_can_xoa = phieu
            else:
                danh_sach_con_lai.append(phieu)

        if phieu_can_xoa is None:
            raise ValueError("Không tìm thấy phiếu: " + ma_phieu)

        self.kiem_tra_kho_duoc_phan_cong(phieu_can_xoa.get("maKho", ""))

        return phieu_can_xoa, danh_sach_con_lai

    def tao_ma_tu_dong(
        self,
        danh_sach,
        truong_ma,
        tien_to,
    ):
        so_lon_nhat = 0

        for item in danh_sach:
            ma = str(item.get(truong_ma, ""))

            if ma.startswith(tien_to):
                phan_so = ma.replace(tien_to, "")

                if phan_so.isdigit():
                    so_lon_nhat = max(so_lon_nhat, int(phan_so))

        return tien_to + str(so_lon_nhat + 1).zfill(4)

    def la_phieu_luu_tam(self, phieu):
        trang_thai = str(phieu.get("trangThai", "")).strip().lower()

        return trang_thai in [
            "lưu tạm",
            "luu tam",
            "l?u t?m",
            "chưa xác nhận",
            "chua xac nhan",
        ] or "lưu" in trang_thai or "luu" in trang_thai

    def chuyen_so_nguyen(self, value):
        return chuyen_so_nguyen(value)

    def lay_ngay_hien_tai(self):
        return date.today().strftime("%Y-%m-%d")

    def lay_thoi_gian_hien_tai(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
