class TaiKhoan:
    def lay_vai_tro_tai_khoan(self, ma_tai_khoan):
        data = self.doc_json("nguoi_dung.json", {})
        vai_tro_map = {}

        for vai_tro in data.get("vaiTro", []):
            vai_tro_map[vai_tro.get("maVaiTro", "")] = vai_tro.get("tenVaiTro", "")

        ket_qua = []
        for phan_quyen in data.get("phanQuyen", []):
            if phan_quyen.get("maTaiKhoan", "") == ma_tai_khoan:
                ket_qua.append(vai_tro_map.get(phan_quyen.get("maVaiTro", ""), ""))

        return ket_qua

    def la_tai_khoan_admin(self, ma_tai_khoan="", ma_nhan_vien=""):
        data = self.doc_json("nguoi_dung.json", {})

        if ma_tai_khoan == "" and ma_nhan_vien != "":
            for tai_khoan in data.get("taiKhoan", []):
                if tai_khoan.get("maNhanVien", "") == ma_nhan_vien:
                    ma_tai_khoan = tai_khoan.get("maTaiKhoan", "")
                    break

        for ten_vai_tro in self.lay_vai_tro_tai_khoan(ma_tai_khoan):
            if str(ten_vai_tro).lower() in ["admin", "quản trị", "quan tri", "quản trị viên", "quan tri vien"]:
                return True

        return False

    def la_tai_khoan_dang_dung(self, ma_tai_khoan="", ma_nhan_vien=""):
        if ma_tai_khoan != "" and ma_tai_khoan == self.lay_ma_tai_khoan_hien_tai():
            return True

        if ma_nhan_vien != "" and ma_nhan_vien == self.lay_ma_nhan_vien_hien_tai():
            return True

        return False

    def kiem_tra_ten_tai_khoan(self, ten_tai_khoan):
        ten_tai_khoan = str(ten_tai_khoan).strip()

        if ten_tai_khoan == "":
            raise ValueError("Vui lòng nhập tên tài khoản.")

        if len(ten_tai_khoan) < 4:
            raise ValueError("Tên tài khoản phải có ít nhất 4 ký tự.")

        if len(ten_tai_khoan) > 50:
            raise ValueError("Tên tài khoản không được quá 50 ký tự.")

        if " " in ten_tai_khoan:
            raise ValueError("Tên tài khoản không được chứa khoảng trắng.")

        for ky_tu in ten_tai_khoan:
            if not (ky_tu.isalnum() or ky_tu in ["_", "."]):
                raise ValueError("Tên tài khoản chỉ được gồm chữ, số, dấu chấm hoặc dấu gạch dưới.")

        return ten_tai_khoan

    def kiem_tra_mat_khau(self, mat_khau):
        mat_khau = str(mat_khau).strip()

        if mat_khau == "":
            raise ValueError("Vui lòng nhập mật khẩu.")

        if len(mat_khau) < 6:
            raise ValueError("Mật khẩu phải có ít nhất 6 ký tự.")

        if len(mat_khau) > 50:
            raise ValueError("Mật khẩu không được quá 50 ký tự.")

        return mat_khau

    def lay_nhan_vien_theo_ma(self, data, ma_nhan_vien):
        for nhan_vien in data.get("nhanVien", []):
            if nhan_vien.get("maNhanVien", "") == ma_nhan_vien:
                return nhan_vien
        return None

    def lay_nhan_vien_cua_tai_khoan(self, data, ma_tai_khoan):
        for tai_khoan in data.get("taiKhoan", []):
            if tai_khoan.get("maTaiKhoan", "") == ma_tai_khoan:
                return self.lay_nhan_vien_theo_ma(data, tai_khoan.get("maNhanVien", ""))
        return None

    def kiem_tra_nhan_vien_duoc_tao_tai_khoan(self, data, ma_nhan_vien):
        nhan_vien = self.lay_nhan_vien_theo_ma(data, ma_nhan_vien)

        if nhan_vien is None:
            raise ValueError("Nhân viên không tồn tại.")

        if not self.la_hoat_dong(nhan_vien.get("trangThai", "")):
            raise ValueError("Nhân viên chưa hoạt động nên không thể tạo tài khoản.")

    def kiem_tra_nhan_vien_duoc_mo_tai_khoan(self, data, ma_tai_khoan):
        nhan_vien = self.lay_nhan_vien_cua_tai_khoan(data, ma_tai_khoan)

        if nhan_vien is None:
            raise ValueError("Không tìm thấy nhân viên liên kết với tài khoản.")

        if not self.la_hoat_dong(nhan_vien.get("trangThai", "")):
            raise ValueError("Không thể kích hoạt tài khoản khi nhân viên chưa hoạt động.")

    def lay_vai_tro_cua_tai_khoan(self, data, ma_tai_khoan):
        for phan_quyen in data.get("phanQuyen", []):
            if phan_quyen.get("maTaiKhoan", "") == ma_tai_khoan:
                return phan_quyen.get("maVaiTro", "")
        return ""

    def kiem_tra_vai_tro_ton_tai(self, data, ma_vai_tro):
        ma_vai_tro = str(ma_vai_tro).strip()

        if ma_vai_tro == "":
            raise ValueError("Vui lòng chọn vai trò.")

        if self.tim_item(data.get("vaiTro", []), "maVaiTro", ma_vai_tro) is None:
            raise ValueError("Vai trò không tồn tại.")

        return ma_vai_tro

    def kiem_tra_vai_tro_duoc_cap(self, data, ma_vai_tro, ma_tai_khoan=""):
        ma_vai_tro = self.kiem_tra_vai_tro_ton_tai(data, ma_vai_tro)
        vai_tro = self.tim_item(data.get("vaiTro", []), "maVaiTro", ma_vai_tro)
        ten_vai_tro = str(vai_tro.get("tenVaiTro", "")).strip().lower()

        if ten_vai_tro in ["admin", "quản trị", "quan tri", "quản trị viên", "quan tri vien"]:
            raise ValueError("Không được cấp vai trò Admin từ màn hình này.")

        if ten_vai_tro not in ["nhân viên kho", "nhan vien kho", "nhanvienkho", "kế toán", "ke toan", "ketoan"]:
            raise ValueError("Chỉ được cấp vai trò Nhân viên kho hoặc Kế toán.")

        return ma_vai_tro

    def kiem_tra_thong_tin_tai_khoan(self, data, du_lieu, ma_bo_qua="", bat_buoc_nhan_vien_hoat_dong=True):
        ten_tai_khoan = self.kiem_tra_ten_tai_khoan(du_lieu.get("tenTaiKhoan", ""))
        mat_khau = self.kiem_tra_mat_khau(du_lieu.get("matKhau", ""))
        ma_nhan_vien = str(du_lieu.get("maNhanVien", "")).strip()

        if ma_nhan_vien == "":
            raise ValueError("Vui lòng chọn nhân viên.")

        nhan_vien = self.lay_nhan_vien_theo_ma(data, ma_nhan_vien)

        if nhan_vien is None:
            raise ValueError("Nhân viên không tồn tại.")

        if bat_buoc_nhan_vien_hoat_dong and not self.la_hoat_dong(nhan_vien.get("trangThai", "")):
            raise ValueError("Nhân viên chưa hoạt động nên không thể kích hoạt tài khoản.")

        self.kiem_tra_trung_gia_tri(
            data.get("taiKhoan", []),
            "tenTaiKhoan",
            ten_tai_khoan,
            "Tên tài khoản",
            "maTaiKhoan",
            ma_bo_qua,
        )

        for tai_khoan in data.get("taiKhoan", []):
            if tai_khoan.get("maTaiKhoan", "") != ma_bo_qua and tai_khoan.get("maNhanVien", "") == ma_nhan_vien:
                raise ValueError("Nhân viên này đã có tài khoản.")

        du_lieu["tenTaiKhoan"] = ten_tai_khoan
        du_lieu["matKhau"] = mat_khau
        du_lieu["maNhanVien"] = ma_nhan_vien

    def vai_tro_can_phan_cong_kho(self, data, ma_vai_tro):
        vai_tro = self.tim_item(data.get("vaiTro", []), "maVaiTro", ma_vai_tro)

        if vai_tro is None:
            return False

        ten_vai_tro = str(vai_tro.get("tenVaiTro", "")).strip().lower()
        return ten_vai_tro in ["nhân viên kho", "nhan vien kho", "nhanvienkho", "kế toán", "ke toan", "ketoan"]

    def kiem_tra_kho_phan_cong(self, data, ma_kho, bat_buoc=False):
        ma_kho = str(ma_kho).strip()

        if ma_kho == "":
            if bat_buoc:
                raise ValueError("Vui lòng chọn kho phụ trách.")
            return ""

        kho_data = self.doc_json("kho_hang.json", {})

        for kho in kho_data.get("kho", []):
            if kho.get("maKho", "") == ma_kho:
                return ma_kho

        raise ValueError("Kho phụ trách không tồn tại.")

    def cap_nhat_phan_cong_kho(self, data, ma_tai_khoan, ma_kho):
        data["phanCongKho"] = [
            item for item in data.get("phanCongKho", [])
            if item.get("maTaiKhoan", "") != ma_tai_khoan
        ]

        if ma_kho != "":
            data.setdefault("phanCongKho", []).append({
                "maTaiKhoan": ma_tai_khoan,
                "maKho": ma_kho,
                "trangThai": True,
            })

    def khoa_phan_cong_kho(self, data, ma_tai_khoan):
        for phan_cong in data.get("phanCongKho", []):
            if phan_cong.get("maTaiKhoan", "") == ma_tai_khoan:
                phan_cong["trangThai"] = False

    def tao_tai_khoan(self, du_lieu, ma_vai_tro, ma_kho=""):
        data = self.doc_nguoi_dung()
        self.kiem_tra_thong_tin_tai_khoan(data, du_lieu, "", True)
        ma_vai_tro = self.kiem_tra_vai_tro_duoc_cap(data, ma_vai_tro)
        ma_kho = self.kiem_tra_kho_phan_cong(
            data,
            ma_kho,
            self.vai_tro_can_phan_cong_kho(data, ma_vai_tro),
        )

        danh_sach = data.setdefault("taiKhoan", [])
        ma_tai_khoan = self.tao_ma_tu_dong_do_dai(danh_sach, "maTaiKhoan", "TK", 3)

        dong = dict(du_lieu)
        dong["maTaiKhoan"] = ma_tai_khoan

        if str(dong.get("trangThai", "")).strip() == "":
            dong["trangThai"] = "Hoạt động"

        danh_sach.append(dong)
        data.setdefault("phanQuyen", []).append({"maTaiKhoan": ma_tai_khoan, "maVaiTro": ma_vai_tro})
        self.cap_nhat_phan_cong_kho(data, ma_tai_khoan, ma_kho)

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Admin thêm Tài khoản", "Tài khoản", "Thêm " + ma_tai_khoan)

        return dong

    def cap_nhat_tai_khoan(self, ma_tai_khoan, du_lieu, ma_vai_tro, ma_kho=""):
        data = self.doc_nguoi_dung()
        tai_khoan = self.tim_item(data.get("taiKhoan", []), "maTaiKhoan", ma_tai_khoan)

        if tai_khoan is None:
            raise ValueError("Không tìm thấy tài khoản cần sửa.")

        trang_thai_cu = str(tai_khoan.get("trangThai", "")).strip()
        trang_thai_moi = str(du_lieu.get("trangThai", trang_thai_cu)).strip()
        bat_buoc_nhan_vien_hoat_dong = self.la_hoat_dong(trang_thai_moi)

        self.kiem_tra_thong_tin_tai_khoan(
            data,
            du_lieu,
            ma_tai_khoan,
            bat_buoc_nhan_vien_hoat_dong,
        )

        ma_vai_tro = self.kiem_tra_vai_tro_duoc_cap(data, ma_vai_tro, ma_tai_khoan)
        ma_kho = self.kiem_tra_kho_phan_cong(
            data,
            ma_kho,
            self.vai_tro_can_phan_cong_kho(data, ma_vai_tro),
        )

        ma_vai_tro_hien_tai = self.lay_vai_tro_cua_tai_khoan(data, ma_tai_khoan)

        if self.la_tai_khoan_dang_dung(ma_tai_khoan=ma_tai_khoan) and ma_vai_tro != ma_vai_tro_hien_tai:
            raise ValueError("Không thể thay đổi phân quyền của chính tài khoản đang đăng nhập.")

        tai_khoan.update(du_lieu)
        tai_khoan["maTaiKhoan"] = ma_tai_khoan

        da_cap_nhat = False
        for phan_quyen in data.get("phanQuyen", []):
            if phan_quyen.get("maTaiKhoan", "") == ma_tai_khoan:
                phan_quyen["maVaiTro"] = ma_vai_tro
                da_cap_nhat = True
                break

        if not da_cap_nhat:
            data.setdefault("phanQuyen", []).append({"maTaiKhoan": ma_tai_khoan, "maVaiTro": ma_vai_tro})

        if trang_thai_moi == "Không hoạt động":
            self.khoa_phan_cong_kho(data, ma_tai_khoan)
        else:
            self.cap_nhat_phan_cong_kho(data, ma_tai_khoan, ma_kho)

        self.ghi_nguoi_dung(data)

        if self.la_khong_hoat_dong(trang_thai_cu) and self.la_hoat_dong(trang_thai_moi):
            self.ghi_nhat_ky("Admin khôi phục Tài khoản", "Tài khoản", "Khôi phục " + ma_tai_khoan)
        else:
            self.ghi_nhat_ky("Admin sửa Tài khoản", "Tài khoản", "Sửa " + ma_tai_khoan)

        return tai_khoan

    def khoa_mo_tai_khoan(self, ma_tai_khoan):
        if self.la_tai_khoan_dang_dung(ma_tai_khoan=ma_tai_khoan):
            raise ValueError("Không thể khóa/mở chính tài khoản đang đăng nhập.")

        data = self.doc_nguoi_dung()
        tai_khoan = self.tim_item(data.get("taiKhoan", []), "maTaiKhoan", ma_tai_khoan)

        if tai_khoan is None:
            raise ValueError("Không tìm thấy tài khoản đã chọn.")

        trang_thai_moi = self.lay_trang_thai_moi(tai_khoan.get("trangThai", ""))

        if trang_thai_moi == "Hoạt động":
            self.kiem_tra_nhan_vien_duoc_mo_tai_khoan(data, ma_tai_khoan)

        tai_khoan["trangThai"] = trang_thai_moi

        if trang_thai_moi == "Đã khóa":
            self.khoa_phan_cong_kho(data, ma_tai_khoan)

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky(
            "Khóa/Mở khóa",
            "Tài khoản",
            "Cập nhật trạng thái " + ma_tai_khoan + " thành " + trang_thai_moi,
        )

        return trang_thai_moi

    def reset_mat_khau_tai_khoan(self, ma_tai_khoan):
        if self.la_tai_khoan_dang_dung(ma_tai_khoan=ma_tai_khoan):
            raise ValueError("Không thể reset mật khẩu của chính tài khoản đang đăng nhập.")

        data = self.doc_nguoi_dung()
        tai_khoan = self.tim_item(data.get("taiKhoan", []), "maTaiKhoan", ma_tai_khoan)

        if tai_khoan is None:
            raise ValueError("Không tìm thấy tài khoản đã chọn.")

        tai_khoan["matKhau"] = "123456"

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Reset mật khẩu", "Tài khoản", "Reset mật khẩu " + ma_tai_khoan)

        return "123456"

    def xoa_tai_khoan(self, ma_tai_khoan):
        if self.la_tai_khoan_dang_dung(ma_tai_khoan=ma_tai_khoan):
            raise ValueError("Không thể xóa chính tài khoản đang đăng nhập.")

        data = self.doc_nguoi_dung()
        tai_khoan = self.tim_item(data.get("taiKhoan", []), "maTaiKhoan", ma_tai_khoan)

        if tai_khoan is None:
            raise ValueError("Không tìm thấy tài khoản cần xóa.")

        if self.la_khong_hoat_dong(tai_khoan.get("trangThai", "")):
            raise ValueError("Tài khoản này đã không hoạt động.")

        tai_khoan["trangThai"] = "Không hoạt động"
        self.khoa_phan_cong_kho(data, ma_tai_khoan)

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky(
            "Admin xóa mềm Tài khoản",
            "Tài khoản",
            "Chuyển " + ma_tai_khoan + " sang Không hoạt động",
        )

        return tai_khoan