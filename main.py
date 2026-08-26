import flet as ft
import pandas as pd
import io

def main(page: ft.Page):
    page.title = "قارئ ومحرك بحث Excel"
    page.rtl = True
    page.padding = 20
    
    df_data = None

    search_input = ft.TextField(
        label="اكتب الكلمة أو الرقم للبحث...", 
        expand=True, 
        disabled=True,
        hint_text="ادخل نص البحث هنا..."
    )
    results_list = ft.ListView(expand=True, spacing=10)
    status_text = ft.Text("يرجى اختيار ملف Excel من الهاتف للبدء", color="grey")

    # دالة التعامل مع استرجاع الملف من مستعرض ملفات الهاتف
    def on_file_picked(e: ft.FilePickerResultEvent):
        nonlocal df_data
        if e.files and len(e.files) > 0:
            selected_file = e.files[0]
            status_text.value = f"جاري قراءة الملف: {selected_file.name}..."
            page.update()
            
            try:
                if selected_file.path:
                    df_data = pd.read_excel(selected_file.path)
                else:
                    with open(selected_file.path, 'rb') as f:
                        df_data = pd.read_excel(io.BytesIO(f.read()))

                search_input.disabled = False
                status_text.value = f"تم تحميل الملف بنجاح! عدد الصفوف: {len(df_data)}"
                status_text.color = "green"
            except Exception as ex:
                status_text.value = f"حدث خطأ أثناء قراءة الملف: {str(ex)}"
                status_text.color = "red"
            
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    # دالة البحث في كامل جدول البيانات
    def search_data(e):
        if df_data is None or not search_input.value:
            return
        
        query = search_input.value.strip().lower()
        
        mask = df_data.astype(str).apply(lambda row: row.str.lower().str.contains(query).any(), axis=1)
        filtered_df = df_data[mask]
        
        results_list.controls.clear()
        
        if filtered_df.empty:
            results_list.controls.append(
                ft.Text("لا توجد نتائج مطابقة لعملية البحث", color="red")
            )
        else:
            for index, row in filtered_df.iterrows():
                row_items = [f"**{col}**: {val}" for col, val in row.items() if pd.notna(val)]
                row_str = " | ".join(row_items)
                
                results_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Markdown(row_str),
                            padding=12
                        )
                    )
                )
        page.update()

    search_input.on_change = search_data

    # استخدام النصوص المباشرة للأيقونات تفادياً لأخطاء الإصدارات
    pick_button = ft.ElevatedButton(
        "اختيار ملف Excel", 
        icon="folder_open",
        on_click=lambda _: file_picker.pick_files(
            dialog_title="اختر ملف Excel",
            allowed_extensions=["xlsx", "xls"]
        )
    )

    page.add(
        ft.Column([
            ft.Row([pick_button, search_input]),
            status_text,
            ft.Divider(),
            results_list
        ], expand=True)
    )

ft.app(target=main)
