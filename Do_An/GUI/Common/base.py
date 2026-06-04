import calendar
import json
import os
import tkinter as tk
from datetime import date
from tkinter import ttk, messagebox

from Calculator.common import (
    chuyen_so,
    chuyen_so_nguyen,
    dinh_dang_so,
    dinh_dang_so_ngan,
    dinh_dang_tien,
)


class GiaoDienCoSo:
    def __init__(self):
        # =========================
        # MÀU SẮC DÙNG CHUNG
        # =========================
        self.mau_nen = "#F8F5F3"
        self.mau_sidebar = "#B98E7C"
        self.mau_menu = "#AD806D"
        self.mau_menu_hover = "#9F725F"

        self.mau_card = "#FFFFFF"
        self.mau_card_nhe = "#FBF7F5"
        self.mau_vien = "#E8D8D0"

        self.mau_chu_dam = "#3F241B"
        self.mau_chu_phu = "#8D6F63"

        self.mau_them = "#7D9D8C"
        self.mau_sua = "#B98E7C"
        self.mau_xoa = "#B56B6B"
        self.mau_thoat = "#6E554C"
        self.mau_tim_kiem = "#8D6F63"

    # =========================
    # FILE JSON DUNG CHUNG
    # =========================
    @staticmethod
    def lay_thu_muc_goc():
        thu_muc = os.path.dirname(os.path.abspath(__file__))

        while True:
            duong_dan_data = os.path.join(thu_muc, "Data")

            if os.path.exists(duong_dan_data):
                return thu_muc

            thu_muc_cha = os.path.dirname(thu_muc)

            if thu_muc_cha == thu_muc:
                return os.path.dirname(os.path.abspath(__file__))

            thu_muc = thu_muc_cha

    @classmethod
    def lay_duong_dan_data(cls, ten_file):
        return os.path.join(cls.lay_thu_muc_goc(), "Data", ten_file)

    @classmethod
    def doc_json(cls, ten_file, mac_dinh=None):
        duong_dan = cls.lay_duong_dan_data(ten_file)

        if not os.path.exists(duong_dan):
            return mac_dinh

        for encoding in ["utf-8-sig", "utf-8", "cp1258"]:
            try:
                with open(duong_dan, "r", encoding=encoding) as file:
                    return json.load(file)
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue

        return mac_dinh

    @classmethod
    def ghi_json(cls, ten_file, data):
        duong_dan = cls.lay_duong_dan_data(ten_file)

        with open(duong_dan, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    # =========================
    # STYLE
    # =========================
    def cau_hinh_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        self.cau_hinh_style_bang(style)
        self.cau_hinh_style_tab(style)

    def cau_hinh_style_bang(self, style):
        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=42,
            background="white",
            fieldbackground="white",
            foreground=self.mau_chu_dam,
            borderwidth=0,
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background=self.mau_card_nhe,
            foreground=self.mau_chu_dam,
            padding=10,
        )

        style.map(
            "Treeview",
            background=[("selected", "#D8C1B5")],
            foreground=[("selected", self.mau_chu_dam)],
        )

    def cau_hinh_style_tab(self, style):
        style.configure(
            "TNotebook",
            background=self.mau_nen,
            borderwidth=0,
        )

        style.configure(
            "TNotebook.Tab",
            background=self.mau_card_nhe,
            foreground=self.mau_chu_dam,
            padding=(18, 10),
            font=("Segoe UI", 10, "bold"),
        )

        style.map(
            "TNotebook.Tab",
            background=[("selected", self.mau_menu)],
            foreground=[("selected", "white")],
        )

    # =========================
    # WIDGET CƠ BẢN
    # =========================
    def xoa_noi_dung(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def tao_label(self, parent, text, size=11, color=None, bold=False, bg=None):
        if color is None:
            color = self.mau_chu_dam

        if bg is None:
            bg = self.mau_card

        if bold:
            font = ("Segoe UI", size, "bold")
        else:
            font = ("Segoe UI", size)

        label = tk.Label(
            parent,
            text=text,
            bg=bg,
            fg=color,
            font=font,
            anchor="w",
            justify="left",
        )

        return label

    def tao_card(self, parent, bg=None):
        if bg is None:
            bg = self.mau_card

        card = tk.Frame(
            parent,
            bg=bg,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
        )

        return card

    def tao_nut(self, parent, text, command, bg=None):
        if bg is None:
            bg = self.mau_menu

        button = tk.Button(
            parent,
            text=text,
            bg=bg,
            fg="white",
            activebackground=bg,
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
            command=command,
        )

        return button

    # =========================
    # BỐ CỤC TRANG
    # =========================
    def tao_tieu_de_trang(self, parent, title, subtitle=""):
        self.xoa_noi_dung(parent)

        header = tk.Frame(parent, bg=self.mau_nen)
        header.pack(fill="x", padx=28, pady=(26, 12))

        self.tao_label(
            header,
            title,
            size=30,
            color=self.mau_chu_dam,
            bold=True,
            bg=self.mau_nen,
        ).pack(anchor="w")

        if subtitle != "":
            self.tao_label(
                header,
                subtitle,
                size=13,
                color=self.mau_chu_phu,
                bg=self.mau_nen,
            ).pack(anchor="w", pady=(6, 0))

    def tao_khung_noi_dung(self, parent):
        khung = self.tao_card(parent)
        khung.pack(fill="both", expand=True, padx=28, pady=(0, 24))

        ben_trong = tk.Frame(khung, bg=self.mau_card)
        ben_trong.pack(fill="both", expand=True, padx=20, pady=20)

        return ben_trong

    def tao_khung_cuon_doc(self, parent, bg=None):
        if bg is None:
            bg = self.mau_card

        wrapper = tk.Frame(parent, bg=bg)
        wrapper.pack(fill="both", expand=True, padx=0, pady=0)

        canvas = tk.Canvas(
            wrapper,
            bg=bg,
            bd=0,
            highlightthickness=0,
        )
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            wrapper,
            orient="vertical",
            command=canvas.yview,
        )
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        content = tk.Frame(canvas, bg=bg)
        window_id = canvas.create_window((0, 0), window=content, anchor="nw")

        def cap_nhat_vung_cuon(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfigure(window_id, width=canvas.winfo_width())

        def cuon_chuot(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        content.bind("<Configure>", cap_nhat_vung_cuon)
        canvas.bind("<Configure>", cap_nhat_vung_cuon)
        canvas.bind("<Enter>", lambda event: canvas.bind_all("<MouseWheel>", cuon_chuot))
        canvas.bind("<Leave>", lambda event: canvas.unbind_all("<MouseWheel>"))

        return content

    # =========================
    # THANH CÔNG CỤ
    # =========================
    def tao_thanh_cong_cu(
        self,
        parent,
        placeholder,
        tim_kiem,
        them=None,
        sua=None,
        xoa=None,
        buttons=None,
    ):
        toolbar = tk.Frame(parent, bg=self.mau_card)
        toolbar.pack(fill="x", pady=(0, 18))

        button_frame = tk.Frame(toolbar, bg=self.mau_card)
        button_frame.pack(side="left")

        search_frame = tk.Frame(toolbar, bg=self.mau_card)
        search_frame.pack(side="right")

        if buttons is None:
            buttons = self.tao_danh_sach_nut_crud(them, sua, xoa)

        self.tao_cac_nut_toolbar(button_frame, buttons)

        entry = self.tao_o_tim_kiem_toolbar(
            search_frame,
            placeholder,
            tim_kiem,
        )

        return entry

    def tao_danh_sach_nut_crud(self, them=None, sua=None, xoa=None):
        buttons = []

        if them is not None:
            buttons.append({
                "text": "Thêm",
                "command": them,
                "color": self.mau_them,
            })

        if sua is not None:
            buttons.append({
                "text": "Sửa",
                "command": sua,
                "color": self.mau_sua,
            })

        if xoa is not None:
            buttons.append({
                "text": "Xóa",
                "command": xoa,
                "color": self.mau_xoa,
            })

        return buttons

    def tao_cac_nut_toolbar(self, parent, buttons):
        for button in buttons:
            text = button.get("text", "")
            command = button.get("command")
            color = button.get("color", self.mau_menu)

            if text == "" or command is None:
                continue

            self.tao_nut(
                parent,
                text,
                command,
                color,
            ).pack(side="left", padx=(0, 8))

    def tao_o_tim_kiem_toolbar(self, parent, placeholder, tim_kiem):
        search_box = tk.Frame(
            parent,
            bg=self.mau_card_nhe,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
        )
        search_box.pack(side="left", padx=(0, 10))

        entry = tk.Entry(
            search_box,
            font=("Segoe UI", 10),
            bg=self.mau_card_nhe,
            fg=self.mau_chu_phu,
            bd=0,
            width=38,
        )
        entry.pack(padx=14, ipady=11)
        entry.insert(0, placeholder)

        def xu_ly_tim(event=None):
            tu_khoa = entry.get().strip()

            if tu_khoa == placeholder:
                tu_khoa = ""

            tim_kiem(tu_khoa)

        def focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=self.mau_chu_dam)

        def focus_out(event):
            if entry.get().strip() == "":
                entry.insert(0, placeholder)
                entry.config(fg=self.mau_chu_phu)

        self.tao_nut(
            parent,
            "Tìm kiếm",
            xu_ly_tim,
            self.mau_tim_kiem,
        ).pack(side="right")

        entry.bind("<FocusIn>", focus_in)
        entry.bind("<FocusOut>", focus_out)
        entry.bind("<Return>", xu_ly_tim)

        return entry

    # =========================
    # LICH CHON NGAY
    # =========================
    def mo_lich_chon_ngay(self, entry):
        hom_nay = date.today()
        nam_hien_tai = hom_nay.year
        thang_hien_tai = hom_nay.month

        popup = tk.Toplevel(self.root)
        popup.title("Chọn ngày")
        popup.geometry("310x280")
        popup.configure(bg=self.mau_card)
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()

        header = tk.Frame(popup, bg=self.mau_card)
        header.pack(fill="x", padx=12, pady=(12, 8))

        thang_var = tk.IntVar(value=thang_hien_tai)
        nam_var = tk.IntVar(value=nam_hien_tai)

        def ve_lich():
            for widget in grid.winfo_children():
                widget.destroy()

            thang = thang_var.get()
            nam = nam_var.get()
            title.config(text=str(thang).zfill(2) + "/" + str(nam))

            for col, text in enumerate(["T2", "T3", "T4", "T5", "T6", "T7", "CN"]):
                tk.Label(
                    grid,
                    text=text,
                    bg=self.mau_card,
                    fg=self.mau_chu_phu,
                    font=("Segoe UI", 9, "bold"),
                    width=4,
                ).grid(row=0, column=col, pady=(0, 4))

            for row_index, tuan in enumerate(calendar.monthcalendar(nam, thang), start=1):
                for col_index, ngay in enumerate(tuan):
                    if ngay == 0:
                        tk.Label(grid, text="", bg=self.mau_card, width=4).grid(row=row_index, column=col_index)
                        continue

                    def chon_ngay(ngay_chon=ngay):
                        entry.delete(0, tk.END)
                        entry.insert(0, f"{nam_var.get()}-{thang_var.get():02d}-{ngay_chon:02d}")
                        popup.destroy()

                    tk.Button(
                        grid,
                        text=str(ngay),
                        command=chon_ngay,
                        bg=self.mau_card_nhe,
                        fg=self.mau_chu_dam,
                        activebackground="#E8DAD4",
                        activeforeground=self.mau_chu_dam,
                        font=("Segoe UI", 9),
                        bd=0,
                        width=4,
                        pady=4,
                        cursor="hand2",
                    ).grid(row=row_index, column=col_index, padx=2, pady=2)

        def lui_thang():
            thang = thang_var.get()
            nam = nam_var.get()

            if thang == 1:
                thang_var.set(12)
                nam_var.set(nam - 1)
            else:
                thang_var.set(thang - 1)

            ve_lich()

        def toi_thang():
            thang = thang_var.get()
            nam = nam_var.get()

            if thang == 12:
                thang_var.set(1)
                nam_var.set(nam + 1)
            else:
                thang_var.set(thang + 1)

            ve_lich()

        tk.Button(
            header,
            text="<",
            command=lui_thang,
            bg=self.mau_sua,
            fg="white",
            bd=0,
            font=("Segoe UI", 11, "bold"),
            width=4,
            cursor="hand2",
        ).pack(side="left")

        title = tk.Label(
            header,
            text="",
            bg=self.mau_card,
            fg=self.mau_chu_dam,
            font=("Segoe UI", 11, "bold"),
        )
        title.pack(side="left", fill="x", expand=True)

        tk.Button(
            header,
            text=">",
            command=toi_thang,
            bg=self.mau_sua,
            fg="white",
            bd=0,
            font=("Segoe UI", 11, "bold"),
            width=4,
            cursor="hand2",
        ).pack(side="right")

        grid = tk.Frame(popup, bg=self.mau_card)
        grid.pack(padx=12, pady=(0, 12))

        ve_lich()

    # =========================
    # BẢNG
    # =========================
    def tao_bang(self, parent, columns, headings, widths, stretch=True):
        table_frame = tk.Frame(parent, bg=self.mau_card)
        table_frame.pack(fill="both", expand=True)

        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
        )

        scroll_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=table.yview,
        )

        scroll_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=table.xview,
        )

        table.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
        )

        table.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        for index in range(len(columns)):
            table.heading(columns[index], text=headings[index])
            table.column(
                columns[index],
                width=widths[index],
                minwidth=60,
                anchor="w",
                stretch=stretch,
            )

        return table

    def do_du_lieu_vao_bang(self, table, danh_sach, cac_cot):
        self.xoa_du_lieu_bang(table)

        for item in danh_sach:
            gia_tri = []

            for cot in cac_cot:
                gia_tri.append(self.lay_gia_tri_cot(item, cot))

            table.insert("", "end", values=gia_tri)

    def xoa_du_lieu_bang(self, table):
        for row in table.get_children():
            table.delete(row)

    def lay_gia_tri_cot(self, item, cot):
        if isinstance(item, dict):
            return item.get(cot, "")

        return getattr(item, cot, "")

    def lay_ma_dong_dang_chon(self, bang):
        selected = bang.selection()

        if len(selected) == 0:
            return ""

        values = bang.item(selected[0], "values")

        if len(values) == 0:
            return ""

        return values[0]

    def gan_su_kien_click(self, widget, command):
        widget.config(cursor="hand2")
        widget.bind("<Button-1>", lambda event: command())

        for child in widget.winfo_children():
            child.config(cursor="hand2")
            child.bind("<Button-1>", lambda event: command())

    # =========================
    # DINH DANG / CHUYEN DOI SO
    # =========================
    def chuyen_so(self, value):
        return chuyen_so(value)

    def chuyen_so_nguyen(self, value):
        return chuyen_so_nguyen(value)

    def dinh_dang_so(self, value):
        return dinh_dang_so(value)

    def dinh_dang_so_ngan(self, value):
        return dinh_dang_so_ngan(value)

    def dinh_dang_tien(self, value):
        return dinh_dang_tien(value)

    # =========================
    # FORM DÙNG CHUNG
    # =========================
    def tao_cua_so_form(self, title, width, height, parent=None):
        parent_window = parent or getattr(self, "root", None)

        if parent_window is None:
            form = tk.Toplevel()
        else:
            form = tk.Toplevel(parent_window)
            form.transient(parent_window)

        form.title(title)
        form.geometry(str(width) + "x" + str(height))
        form.minsize(width, min(height, 420))
        form.configure(bg=self.mau_card)
        form.grab_set()

        self.tao_label(
            form,
            title,
            size=17,
            color=self.mau_chu_dam,
            bold=True,
            bg=self.mau_card,
        ).pack(anchor="w", padx=22, pady=(16, 8))

        body = tk.Frame(form, bg=self.mau_card)
        body.pack(fill="both", expand=True, padx=22, pady=(0, 8))

        bottom = tk.Frame(form, bg=self.mau_card)
        bottom.pack(side="bottom", fill="x", padx=22, pady=(4, 16))

        return {
            "window": form,
            "body": body,
            "bottom": bottom,
        }

    def tao_combobox_form(self, parent, label_text, values):
        self.tao_label(
            parent,
            label_text,
            size=10,
            color=self.mau_chu_phu,
            bold=True,
        ).pack(anchor="w", pady=(5, 2))

        combo = ttk.Combobox(
            parent,
            values=values,
            state="readonly",
            font=("Segoe UI", 10),
        )
        combo.pack(fill="x", ipady=3)

        if len(values) > 0:
            combo.current(0)

        return combo

    def tao_entry_form(self, parent, label_text):
        self.tao_label(
            parent,
            label_text,
            size=10,
            color=self.mau_chu_phu,
            bold=True,
        ).pack(anchor="w", pady=(5, 2))

        entry = tk.Entry(
            parent,
            font=("Segoe UI", 10),
            bg=self.mau_card_nhe,
            fg=self.mau_chu_dam,
            bd=0,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
        )
        entry.pack(fill="x", ipady=6)

        return entry

    def tao_nut_luu_huy(self, parent, luu, huy, text_luu="Lưu", text_huy="Hủy"):
        self.tao_nut(
            parent,
            text_luu,
            luu,
            self.mau_them,
        ).pack(side="right", padx=(8, 0))

        self.tao_nut(
            parent,
            text_huy,
            huy,
            self.mau_thoat,
        ).pack(side="right")

    def tao_danh_sach_chon(self, danh_sach, ma_key, ten_key):
        ket_qua = []

        for item in danh_sach:
            ma = str(self.lay_gia_tri_cot(item, ma_key))
            ten = str(self.lay_gia_tri_cot(item, ten_key))

            ket_qua.append(ma + " - " + ten)

        return ket_qua

    def lay_ma_tu_combobox(self, value):
        if value is None:
            return ""

        value = str(value).strip()

        if value == "":
            return ""

        return value.split(" - ", 1)[0].strip()

    def chon_combobox_theo_ma(self, combo, ma):
        values = list(combo.cget("values"))

        for index, value in enumerate(values):
            dung_ma_day_du = str(value).startswith(str(ma) + " -")
            dung_ma_truc_tiep = str(value) == str(ma)

            if dung_ma_day_du or dung_ma_truc_tiep:
                combo.current(index)
                return

    # =========================
    # NÚT THOÁT / THÔNG BÁO
    # =========================
    def tao_nut_thoat_duoi(self, parent, command):
        bottom = tk.Frame(parent, bg=self.mau_card)
        bottom.pack(fill="x", pady=(16, 0))

        self.tao_nut(
            bottom,
            "Thoát",
            command,
            self.mau_thoat,
        ).pack(side="right")

