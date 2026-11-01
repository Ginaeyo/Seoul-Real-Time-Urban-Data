"""콘솔에서 사용자가 조회할 지역을 선택하는 모듈.

TODO(담당: 김효중)
- AreaManager의 지역 목록을 보여 주고 번호 입력을 받는다.
- 숫자가 아닌 입력과 범위를 벗어난 번호를 안전하게 처리한다.
- select_location()은 선택된 Place 또는 실패 시 None을 반환한다.
"""
"""서울 지역 선택 창: 전체 목록 클릭 또는 검색 후 클릭."""
import tkinter as tk
from tkinter import ttk, messagebox


class LocationSelector:
    def __init__(self, area_manager):
        self.area_manager = area_manager
        self.Selected_area = None  # 최종 선택된 지역명
        self.search_keyword = ""
        self.comparison_areas = []

    def selected_location(self, area):
        """선택 지역명(또는 Place 객체)을 저장하고 지역명 반환."""
        if area is None:
            self.Selected_area = None
            return None
        name = area.area_name if hasattr(area, "area_name") else str(area)
        # 선택 이름을 실제 Place 목록에서 검증
        if self.area_manager.get_area(name) is None:
            return None
        self.Selected_area = name
        return self.Selected_area

    def select_comparison_areas(self, parent=None):
        """기존 지역 선택창을 두 번 사용하여 서로 다른 두 지역명을 반환."""
        self.comparison_areas = []
        first = self.search_location(parent=parent)
        if first is None:
            return None
        while True:
            second = self.search_location(parent=parent)
            if second is None:
                self.comparison_areas = []
                return None
            if first == second:
                messagebox.showwarning("지역 선택 오류", "서로 다른 두 지역을 선택하세요.", parent=parent)
                continue
            self.comparison_areas = [first, second]
            return list(self.comparison_areas)

    # 제안서에 표기된 select_location()으로도 사용할 수 있도록 별칭 제공
    def select_location(self, area):
        return self.selected_location(area)

    def search_location(self, parent=None):
        """지역 선택 창을 열고, 사용자 선택이 끝나면 지역명 문자열 반환.

        취소하면 None을 반환합니다. 창이 열려 있는 동안 텍스트 검색과
        목록 선택은 모두 동일한 목록에 반영됩니다.
        """
        self.Selected_area = None
        self.search_keyword = ""
        self._filtered_areas = self.area_manager.get_areas()

        is_root = parent is None
        window = tk.Tk() if is_root else tk.Toplevel(parent)
        window.title("서울 실시간 도시데이터 - 지역 선택")
        window.geometry("530x540")
        window.minsize(410, 380)
        window.resizable(True, True)

        frame = ttk.Frame(window, padding=16)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="조회할 지역을 선택하세요", font=("맑은 고딕", 14, "bold")).pack(anchor="w")
        ttk.Label(frame, text="전체 목록에서 선택하거나 지역명을 검색하세요.").pack(anchor="w", pady=(6, 12))

        keyword_var = tk.StringVar()
        search_entry = ttk.Entry(frame, textvariable=keyword_var)
        search_entry.pack(fill="x", pady=(0, 10))

        result_count = ttk.Label(frame)
        result_count.pack(anchor="w", pady=(0, 5))

        list_frame = ttk.Frame(frame)
        list_frame.pack(fill="both", expand=True)
        listbox = tk.Listbox(list_frame, height=16, exportselection=False, font=("맑은 고딕", 10))
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def refresh(*_):
            self.search_keyword = keyword_var.get().strip()
            self._filtered_areas = self.area_manager.search_areas(self.search_keyword)
            listbox.delete(0, tk.END)
            for area in self._filtered_areas:
                listbox.insert(tk.END, f"{area.area_code}. {area.area_name}")
            result_count.config(text=f"검색 결과: {len(self._filtered_areas)}개")

        def confirm(_=None):
            indices = listbox.curselection()
            if not indices:
                messagebox.showwarning("지역 미선택", "목록에서 지역 하나를 선택하세요.", parent=window)
                return
            place = self._filtered_areas[indices[0]]
            self.selected_location(place)
            window.destroy()

        def cancel():
            self.Selected_area = None
            window.destroy()

        buttons = ttk.Frame(frame)
        buttons.pack(fill="x", pady=(12, 0))
        ttk.Button(buttons, text="선택", command=confirm).pack(side="right")
        ttk.Button(buttons, text="취소", command=cancel).pack(side="right", padx=(0, 8))

        keyword_var.trace_add("write", refresh)
        listbox.bind("<Double-Button-1>", confirm)
        listbox.bind("<Return>", confirm)
        window.protocol("WM_DELETE_WINDOW", cancel)
        refresh()
        search_entry.focus_set()
        if parent is not None:
            window.transient(parent)
            window.grab_set()
            parent.wait_window(window)
        else:
            window.mainloop()
        return self.Selected_area
