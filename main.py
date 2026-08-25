import flet as ft
import pandas as pd
import os

def main(page: ft.Page):
    page.title = "مستودع قطع الغيار"
    page.theme_mode = ft.ThemeMode.DARK  # متوافق مع Dark Mode الخاص بـ HyperOS
    page.padding = 15
    page.vertical_alignment = ft.MainAxisAlignment.START

    # متغير لتخزين بيانات الإكسل
    df = None

    # نافذة عرض النتائج
    results_list = ft.ListView(expand=1, spacing=10, padding=0)

    def load_excel():
        nonlocal df
        # يمكنك وضع اسم ملف الإكسل بجانب السكربت أو جعله يختاره
        file_path = "warehouse.xlsx" 
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
            # التأكد من تطابق الأعمدة تماماً مع صورتك
            df.columns = ["الرمز", "اسم المادة", "مفتاح 1", "مفتاح 2", "مفتاح 3", "وحدة القياس", "الرصيد الحالي"]
            show_data(df)
        else:
            results_list.controls.clear()
            results_list.controls.append(
                ft.Text("⚠️ ملف الإكسل غير موجود، يرجى وضع الملف باسم warehouse.xlsx", color="red")
            )
            page.update()

    def show_data(data_frame):
        results_list.controls.clear()
        for index, row in data_frame.iterrows():
            card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"الرمز: {row['الرمز']}", weight=ft.FontWeight.BOLD, color="blue_400"),
                        ft.Text(f"الرصيد: {row['الرصيد الحالي']} {row['وحدة القياس']}", weight=ft.FontWeight.BOLD, color="green_400")
                    ], alignment=ft.MainAxisAlignment.BETWEEN),
                    ft.Text(f"{row['اسم المادة']}", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"التصنيف: {row['مفتاح 1']} / {row['مفتاح 2']} / {row['مفتاح 3']}", size=12, color="grey_400"),
                ]),
                padding=12,
                border_radius=10,
                bgcolor=ft.colors.SURFACE_VARIANT,
                margin=ft.margin.only(bottom=5)
            )
            results_list.controls.append(card)
        page.update()

    def search_items(e):
        nonlocal df
        if df is not None:
            query = search_box.value.lower()
            # البحث في الرمز أو اسم المادة
            filtered_df = df[
                df['اسم المادة'].astype(str).str.lower().str.contains(query, na=False) |
                df['الرمز'].astype(str).str.lower().str.contains(query, na=False)
            ]
            show_data(filtered_df)

    search_box = ft.TextField(
        label="ابحث برمز المادة أو اسمها...",
        prefix_icon=ft.icons.SEARCH,
        on_change=search_items,
        border_radius=10
    )

    page.add(
        ft.Text("مستعرض المستودع الرقمي", size=20, weight=ft.FontWeight.BOLD),
        search_box,
        results_list
    )

    load_excel()

ft.app(target=main)
