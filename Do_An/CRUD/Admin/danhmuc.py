class DanhMuc:
    def kiem_tra_sdt(self, value, label="Số điện thoại", bat_buoc=False):
        value = str(value).strip()

        if value == "":
            if bat_buoc:
                raise ValueError("Vui lòng nhập " + label.lower() + ".")
            return ""

        if not value.isdigit():
            raise ValueError(label + " chỉ được nhập số.")

        if len(value) != 10:
            raise ValueError(label + " phải gồm đúng 10 số.")

        if not value.startswith("0"):
            raise ValueError(label + " phải bắt đầu bằng số 0.")

        return value

    def kiem_tra_email(self, value, label="Email", bat_buoc=False):
        value = str(value).strip()

        if value == "":
            if bat_buoc:
                raise ValueError("Vui lòng nhập " + label.lower() + ".")
            return ""

        if " " in value:
            raise ValueError(label + " không được chứa khoảng trắng.")

        if not value.endswith("@gmail.com"):
            raise ValueError(label + " phải có dạng example@gmail.com.")

        ten_email = value.replace("@gmail.com", "")

        if ten_email == "":
            raise ValueError(label + " không hợp lệ.")

        return value

    def kiem_tra_ten_danh_muc(self, value, label):
        value = str(value).strip()

        if value == "":
            raise ValueError("Vui lòng nhập " + label.lower() + ".")

        if len(value) < 2:
            raise ValueError(label + " phải có ít nhất 2 ký tự.")

        if len(value) > 100:
            raise ValueError(label + " không được quá 100 ký tự.")

        return value

    def kiem_tra_dia_chi(self, value, bat_buoc=True):
        value = str(value).strip()

        if value == "":
            if bat_buoc:
                raise ValueError("Vui lòng nhập địa chỉ.")
            return ""

        if len(value) < 3:
            raise ValueError("Địa chỉ phải có ít nhất 3 ký tự.")

        if len(value) > 200:
            raise ValueError("Địa chỉ không được quá 200 ký tự.")

        return value

    def kiem_tra_ghi_chu(self, value):
        value = str(value).strip()

        if len(value) > 200:
            raise ValueError("Ghi chú không được quá 200 ký tự.")

        return value

    def kiem_tra_danh_muc_truoc_luu(self, data, danh_muc, truong_ma, ma_bo_qua, du_lieu):
        danh_sach = data.get(danh_muc, [])

        cau_hinh_ten = {
            "kho": ("tenKho", "Tên kho"),
            "loaiHang": ("tenLoaiHang", "Tên loại hàng"),
            "donViTinh": ("tenDonViTinh", "Tên đơn vị tính"),
            "nhaSanXuat": ("tenNhaSanXuat", "Tên nhà sản xuất"),
            "khachHang": ("tenKhachHang", "Tên khách hàng"),
        }

        if danh_muc in cau_hinh_ten:
            truong_ten, ten_truong = cau_hinh_ten[danh_muc]
            ten = self.kiem_tra_ten_danh_muc(du_lieu.get(truong_ten, ""), ten_truong)
            du_lieu[truong_ten] = ten

            self.kiem_tra_trung_gia_tri(
                danh_sach,
                truong_ten,
                ten,
                ten_truong,
                truong_ma,
                ma_bo_qua,
            )

        if danh_muc == "kho":
            du_lieu["soDienThoai"] = self.kiem_tra_sdt(
                du_lieu.get("soDienThoai", ""),
                "Số điện thoại",
                False,
            )

            self.kiem_tra_trung_gia_tri(
                danh_sach,
                "soDienThoai",
                du_lieu.get("soDienThoai", ""),
                "Số điện thoại",
                truong_ma,
                ma_bo_qua,
            )

            if "diaDiem" in du_lieu:
                du_lieu["diaDiem"] = self.kiem_tra_dia_chi(
                    du_lieu.get("diaDiem", ""),
                    True,
                )

        if danh_muc in ["nhaSanXuat", "khachHang"]:
            du_lieu["soDienThoai"] = self.kiem_tra_sdt(
                du_lieu.get("soDienThoai", ""),
                "Số điện thoại",
                False,
            )

            du_lieu["email"] = self.kiem_tra_email(
                du_lieu.get("email", ""),
                "Email",
                False,
            )

            self.kiem_tra_trung_gia_tri(
                danh_sach,
                "soDienThoai",
                du_lieu.get("soDienThoai", ""),
                "Số điện thoại",
                truong_ma,
                ma_bo_qua,
            )

            self.kiem_tra_trung_gia_tri(
                danh_sach,
                "email",
                du_lieu.get("email", ""),
                "Email",
                truong_ma,
                ma_bo_qua,
            )

            du_lieu["diaChi"] = self.kiem_tra_dia_chi(
                du_lieu.get("diaChi", ""),
                True,
            )

        if "ghiChu" in du_lieu:
            du_lieu["ghiChu"] = self.kiem_tra_ghi_chu(du_lieu.get("ghiChu", ""))

    def them_danh_muc_json(self, ten_file, danh_muc, truong_ma, tien_to, du_lieu, ten_doi_tuong, do_dai_so=4):
        data = self.doc_json(ten_file, {})
        danh_sach = data.setdefault(danh_muc, [])

        self.kiem_tra_danh_muc_truoc_luu(
            data,
            danh_muc,
            truong_ma,
            "",
            du_lieu,
        )

        ma_moi = self.tao_ma_tu_dong_do_dai(
            danh_sach,
            truong_ma,
            tien_to,
            do_dai_so,
        )

        dong = dict(du_lieu)
        dong[truong_ma] = ma_moi

        danh_sach.append(dong)

        self.ghi_json(ten_file, data)
        self.ghi_nhat_ky("Admin thêm " + ten_doi_tuong, ten_doi_tuong, "Thêm " + ma_moi)

        return dong

    def sua_danh_muc_json(self, ten_file, danh_muc, truong_ma, ma, du_lieu, ten_doi_tuong):
        data = self.doc_json(ten_file, {})
        item = self.tim_item(data.get(danh_muc, []), truong_ma, ma)

        if item is None:
            raise ValueError("Không tìm thấy dữ liệu cần sửa.")

        self.kiem_tra_danh_muc_truoc_luu(
            data,
            danh_muc,
            truong_ma,
            ma,
            du_lieu,
        )

        item.update(du_lieu)
        item[truong_ma] = ma

        self.ghi_json(ten_file, data)
        self.ghi_nhat_ky("Admin sửa " + ten_doi_tuong, ten_doi_tuong, "Sửa " + ma)

        return item

    def tao_thong_bao_dang_duoc_su_dung(self, ten_doi_tuong, ma, danh_sach_lien_quan):
        return (
            "Không thể xóa "
            + ten_doi_tuong
            + " "
            + ma
            + " vì đang được sử dụng: "
            + ", ".join(danh_sach_lien_quan)
            + "."
        )

    def kiem_tra_truoc_xoa_danh_muc(self, ten_file, danh_muc, ma, ten_doi_tuong):
        lien_quan = []

        if ten_file == "hang_hoa.json" and danh_muc == "donViTinh":
            hang_data = self.doc_json("hang_hoa.json", {})
            so_san_pham = self.dem_dong_theo_ma(hang_data.get("sanPham", []), "maDonViTinh", ma)

            if so_san_pham > 0:
                lien_quan.append(str(so_san_pham) + " sản phẩm")

        if ten_file == "doi_tac.json" and danh_muc == "khachHang":
            phieu_xuat = self.doc_json("phieu_xuat.json", [])
            so_phieu_xuat = self.dem_dong_theo_ma(phieu_xuat, "maKhachHang", ma)

            if so_phieu_xuat > 0:
                lien_quan.append(str(so_phieu_xuat) + " phiếu xuất")

        if len(lien_quan) > 0:
            raise ValueError(
                self.tao_thong_bao_dang_duoc_su_dung(
                    ten_doi_tuong.lower(),
                    ma,
                    lien_quan,
                )
            )

    def xoa_danh_muc_json(self, ten_file, danh_muc, truong_ma, ma, ten_doi_tuong):
        self.kiem_tra_truoc_xoa_danh_muc(
            ten_file,
            danh_muc,
            ma,
            ten_doi_tuong,
        )

        data = self.doc_json(ten_file, {})
        danh_sach = data.get(danh_muc, [])
        con_lai = []
        da_tim_thay = False

        for item in danh_sach:
            if item.get(truong_ma, "") == ma:
                da_tim_thay = True
            else:
                con_lai.append(item)

        if not da_tim_thay:
            raise ValueError("Không tìm thấy dữ liệu cần xóa.")

        data[danh_muc] = con_lai

        self.ghi_json(ten_file, data)
        self.ghi_nhat_ky("Admin xóa " + ten_doi_tuong, ten_doi_tuong, "Xóa " + ma)

        return True

    def xoa_kho(self, ma_kho):
        kho_data = self.doc_json("kho_hang.json", {})
        nguoi_dung = self.doc_json("nguoi_dung.json", {})
        phieu_nhap = self.doc_json("phieu_nhap.json", [])
        phieu_xuat = self.doc_json("phieu_xuat.json", [])
        kiem_ke = self.doc_json("kiem_ke.json", [])
        canh_bao = self.doc_json("canh_bao.json", [])

        lien_quan = []

        so_ton = self.dem_dong_theo_ma(kho_data.get("tonKho", []), "maKho", ma_kho)
        so_vi_tri = self.dem_dong_theo_ma(kho_data.get("viTriKho", []), "maKho", ma_kho)
        so_phan_cong = self.dem_dong_theo_ma(nguoi_dung.get("phanCongKho", []), "maKho", ma_kho)
        so_phieu_nhap = self.dem_dong_theo_ma(phieu_nhap, "maKho", ma_kho)
        so_phieu_xuat = self.dem_dong_theo_ma(phieu_xuat, "maKho", ma_kho)
        so_kiem_ke = self.dem_dong_theo_ma(kiem_ke, "maKho", ma_kho)
        so_canh_bao = self.dem_dong_theo_ma(canh_bao, "maKho", ma_kho)

        if so_ton > 0:
            lien_quan.append(str(so_ton) + " dòng tồn kho")
        if so_vi_tri > 0:
            lien_quan.append(str(so_vi_tri) + " vị trí kho")
        if so_phan_cong > 0:
            lien_quan.append(str(so_phan_cong) + " phân công kho")
        if so_phieu_nhap > 0:
            lien_quan.append(str(so_phieu_nhap) + " phiếu nhập")
        if so_phieu_xuat > 0:
            lien_quan.append(str(so_phieu_xuat) + " phiếu xuất")
        if so_kiem_ke > 0:
            lien_quan.append(str(so_kiem_ke) + " phiếu kiểm kê")
        if so_canh_bao > 0:
            lien_quan.append(str(so_canh_bao) + " cảnh báo tồn kho")

        if len(lien_quan) > 0:
            raise ValueError(
                self.tao_thong_bao_dang_duoc_su_dung(
                    "kho",
                    ma_kho,
                    lien_quan,
                )
            )

        return self.xoa_danh_muc_json(
            "kho_hang.json",
            "kho",
            "maKho",
            ma_kho,
            "Kho",
        )

    def xoa_loai_hang(self, ma_loai_hang):
        hang_data = self.doc_json("hang_hoa.json", {})
        so_san_pham = self.dem_dong_theo_ma(
            hang_data.get("sanPham", []),
            "maLoaiHang",
            ma_loai_hang,
        )

        if so_san_pham > 0:
            raise ValueError(
                self.tao_thong_bao_dang_duoc_su_dung(
                    "loại hàng",
                    ma_loai_hang,
                    [str(so_san_pham) + " sản phẩm"],
                )
            )

        return self.xoa_danh_muc_json(
            "hang_hoa.json",
            "loaiHang",
            "maLoaiHang",
            ma_loai_hang,
            "Loại hàng",
        )

    def xoa_nha_san_xuat(self, ma_nha_san_xuat):
        phieu_nhap = self.doc_json("phieu_nhap.json", [])
        so_phieu_nhap = self.dem_dong_theo_ma(
            phieu_nhap,
            "maNhaSanXuat",
            ma_nha_san_xuat,
        )

        if so_phieu_nhap > 0:
            raise ValueError(
                self.tao_thong_bao_dang_duoc_su_dung(
                    "nhà sản xuất",
                    ma_nha_san_xuat,
                    [str(so_phieu_nhap) + " phiếu nhập"],
                )
            )

        return self.xoa_danh_muc_json(
            "doi_tac.json",
            "nhaSanXuat",
            "maNhaSanXuat",
            ma_nha_san_xuat,
            "Nhà sản xuất",
        )