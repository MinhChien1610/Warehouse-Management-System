class TaiKhoan:
    def lay_vai_tro_tai_khoan(self, ma_tai_khoan):
        data = self.doc_json("nguoi_dung.json", {})
        vai_tro_map = {}

        for vai_tro in data.get("vaiTro", []):
            vai_tro_map[vai_tro.get("maVaiTro", "")] = vai_tro.get("tenVaiTro", "")

        ket_qua = []
        for phan_quyen in data.get("phanQuyen", []):
            if phan_quyen.get("maTaiKhoan") == ma_tai_khoan:
                ket_qua.append(vai_tro_map.get(phan_quyen.get("maVaiTro", ""), ""))

        return ket_qua

    def la_tai_khoan_admin(self, ma_tai_khoan="", ma_nhan_vien=""):
        data = self.doc_json("nguoi_dung.json", {})

        if ma_tai_khoan == "" and ma_nhan_vien != "":
            for tai_khoan in data.get("taiKhoan", []):
                if tai_khoan.get("maNhanVien") == ma_nhan_vien:
                    ma_tai_khoan = tai_khoan.get("maTaiKhoan", "")
                    break

        for ten_vai_tro in self.lay_vai_tro_tai_khoan(ma_tai_khoan):
            if str(ten_vai_tro).lower() in ["admin", "quan tri", "quan tri vien"]:
                return True

        return False

    def la_tai_khoan_dang_dung(self, ma_tai_khoan="", ma_nhan_vien=""):
        if ma_tai_khoan != "" and ma_tai_khoan == self.lay_ma_tai_khoan_hien_tai():
            return True

        if ma_nhan_vien != "" and ma_nhan_vien == self.lay_ma_nhan_vien_hien_tai():
            return True

        return False

    def kiem_tra_thong_tin_tai_khoan(self, data, du_lieu, ma_bo_qua=""):
        ten_tai_khoan = str(du_lieu.get("tenTaiKhoan", "")).strip()
        mat_khau = str(du_lieu.get("matKhau", "")).strip()
        ma_nhan_vien = du_lieu.get("maNhanVien", "")

        if ten_tai_khoan == "":
            raise ValueError("Vui lòng nhập tên tài khoản.")

        if mat_khau == "":
            raise ValueError("Vui lòng nhập mật khẩu.")

        if len(mat_khau) < 6:
            raise ValueError("Mật khẩu phải có ít nhất 6 ký tự.")

        if ma_nhan_vien == "":
            raise ValueError("Vui lòng chọn nhân viên.")

        if self.tim_item(data.get("nhanVien", []), "maNhanVien", ma_nhan_vien) is None:
            raise ValueError("Nhân viên không tồn tại.")

        self.kiem_tra_trung_gia_tri(data.get("taiKhoan", []), "tenTaiKhoan", ten_tai_khoan, "Tên tài khoản", "maTaiKhoan", ma_bo_qua)

        for tai_khoan in data.get("taiKhoan", []):
            if tai_khoan.get("maTaiKhoan", "") != ma_bo_qua and tai_khoan.get("maNhanVien", "") == ma_nhan_vien:
                raise ValueError("Nhân viên này đã có tài khoản.")

    def kiem_tra_vai_tro_ton_tai(self, data, ma_vai_tro):
        if ma_vai_tro == "":
            raise ValueError("Vui lòng chọn vai trò.")

        if self.tim_item(data.get("vaiTro", []), "maVaiTro", ma_vai_tro) is None:
            raise ValueError("Vai trò không tồn tại.")

    def tao_tai_khoan(self, du_lieu, ma_vai_tro):
        data = self.doc_nguoi_dung()
        self.kiem_tra_thong_tin_tai_khoan(data, du_lieu)
        self.kiem_tra_vai_tro_ton_tai(data, ma_vai_tro)

        danh_sach = data.setdefault("taiKhoan", [])
        ma_tai_khoan = self.tao_ma_tu_dong_do_dai(danh_sach, "maTaiKhoan", "TK", 3)

        dong = dict(du_lieu)
        dong["maTaiKhoan"] = ma_tai_khoan

        if dong.get("trangThai", "") == "":
            dong["trangThai"] = "Hoạt động"

        danh_sach.append(dong)
        data.setdefault("phanQuyen", []).append({"maTaiKhoan": ma_tai_khoan, "maVaiTro": ma_vai_tro})

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Admin thêm Tài khoản", "Tài khoản", "Thêm " + ma_tai_khoan)
        return dong

    def cap_nhat_tai_khoan(self, ma_tai_khoan, du_lieu, ma_vai_tro):
        data = self.doc_nguoi_dung()
        self.kiem_tra_thong_tin_tai_khoan(data, du_lieu, ma_tai_khoan)
        self.kiem_tra_vai_tro_ton_tai(data, ma_vai_tro)

        tai_khoan = self.tim_item(data.get("taiKhoan", []), "maTaiKhoan", ma_tai_khoan)

        if tai_khoan is None:
            raise ValueError("Không tìm thấy tài khoản cần sửa.")

        tai_khoan.update(du_lieu)
        tai_khoan["maTaiKhoan"] = ma_tai_khoan

        da_cap_nhat = False
        for phan_quyen in data.get("phanQuyen", []):
            if phan_quyen.get("maTaiKhoan") == ma_tai_khoan:
                phan_quyen["maVaiTro"] = ma_vai_tro
                da_cap_nhat = True
                break

        if not da_cap_nhat:
            data.setdefault("phanQuyen", []).append({"maTaiKhoan": ma_tai_khoan, "maVaiTro": ma_vai_tro})

        self.ghi_nguoi_dung(data)
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
        tai_khoan["trangThai"] = trang_thai_moi

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Khóa/Mở khóa", "Tài khoản", "Cập nhật trạng thái " + ma_tai_khoan + " thành " + trang_thai_moi)
        return trang_thai_moi

    def reset_mat_khau_tai_khoan(self, ma_tai_khoan):
        if self.la_tai_khoan_dang_dung(ma_tai_khoan=ma_tai_khoan):
            raise ValueError("Không thể reset mật khẩu của chính tài khoản đang đăng nhập.")

        data = self.doc_nguoi_dung()
        tai_khoan = self.tim_item(data.get("taiKhoan", []), "maTaiKhoan", ma_tai_khoan)

        if tai_khoan is None:
            raise ValueError("Không tìm thấy tài khoản đã chọn.")

        mat_khau_moi = "123456"
        tai_khoan["matKhau"] = mat_khau_moi

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Reset mật khẩu", "Tài khoản", "Reset mật khẩu " + ma_tai_khoan)
        return mat_khau_moi

    def xoa_tai_khoan(self, ma_tai_khoan):
        if self.la_tai_khoan_dang_dung(ma_tai_khoan=ma_tai_khoan):
            raise ValueError("Không thể xóa chính tài khoản đang đăng nhập.")

        data = self.doc_nguoi_dung()
        tai_khoan = self.tim_item(data.get("taiKhoan", []), "maTaiKhoan", ma_tai_khoan)

        if tai_khoan is None:
            raise ValueError("Không tìm thấy tài khoản cần xóa.")

        if not self.la_trang_thai_khoa(tai_khoan.get("trangThai", "")):
            raise ValueError("Chỉ được xóa tài khoản đang ở trạng thái Đã khóa.")

        data["taiKhoan"] = [item for item in data.get("taiKhoan", []) if item.get("maTaiKhoan", "") != ma_tai_khoan]
        data["phanQuyen"] = [item for item in data.get("phanQuyen", []) if item.get("maTaiKhoan", "") != ma_tai_khoan]
        data["phanCongKho"] = [item for item in data.get("phanCongKho", []) if item.get("maTaiKhoan", "") != ma_tai_khoan]

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Admin xóa Tài khoản", "Tài khoản", "Xóa " + ma_tai_khoan)
        return tai_khoan
