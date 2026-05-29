from __future__ import annotations

import json
import os
from copy import deepcopy
from datetime import date, datetime
from typing import Any, Dict, List, Tuple

from Class.nhatky import NhatKy


class NhatKy:
    def ghi_nhat_ky(self, hanh_dong: str, doi_tuong: str, ghi_chu: str):
        data = self.doc_json("nhat_ky.json", [])
        ma_nhat_ky = self.tao_ma_tu_dong(data, "maNhatKy", "NK")

        nhat_ky = NhatKy(
            ma_nhat_ky,
            self.ma_tai_khoan,
            hanh_dong,
            doi_tuong,
            self.lay_thoi_gian_hien_tai(),
            "Th?nh c?ng",
            ghi_chu,
        ).to_dict()

        data.append(nhat_ky)
        self.ghi_json("nhat_ky.json", data)

        return nhat_ky

    # =========================
    # KIỂM TRA DỮ LIỆU
    # =========================
