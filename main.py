import os
import sqlite3
import pandas as pd
import arabic_reshaper
from bidi.algorithm import get_display
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.clock import Clock
from plyer import camera, filechooser

# 1. تسجيل الخط العربي لضمان القراءة الصحيحة على الأندرويد
# تأكد من رفع ملف الخط باسم 'alfont_com_arial-1.ttf' في نفس المجلد
try:
    LabelBase.register(name='ArabicFont', fn_regular='alfont_com_arial-1.ttf')
except Exception as e:
    print(f"Font Error: {e}")

def ar(text):
    if not text: return ""
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

# واجهة المستخدم KV
KV = f"""
<Label>:
    font_name: 'ArabicFont'

<Button>:
    font_name: 'ArabicFont'

<TextInput>:
    font_name: 'ArabicFont'

<SpinnerOption>:
    font_name: 'ArabicFont'
    font_size: '16sp'
    height: "50dp"

<BeneficiaryButton@Button>:
    background_normal: ''
    background_color: 1, 1, 1, 1
    color: 0, 0, 0, 1
    size_hint_y: None
    height: "80dp"
    font_size: '18sp'

ScreenManager:
    SearchScreen:
    SurveyScreen:

<SearchScreen>:
    name: 'search'
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 0.95, 0.95, 0.95, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        BoxLayout:
            size_hint_y: None
            height: "65dp"
            padding: "10dp"
            canvas.before:
                Color:
                    rgba: 0.1, 0.3, 0.5, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: "{ar('إحصاء 2026 - نسيم حميتي')}"
                bold: True
                font_size: '20sp'

        BoxLayout:
            size_hint_y: None
            height: "55dp"
            spacing: "5dp"
            padding: "5dp"
            Button:
                text: "{ar('📥 استيراد قائمة')}"
                background_color: 0.2, 0.3, 0.5, 1
                on_release: app.import_new_data()
            Button:
                text: "{ar('📈 جدول الإحصاء')}"
                background_color: 0.8, 0.4, 0.1, 1
                on_release: app.export_stats()

        BoxLayout:
            size_hint_y: None
            height: "55dp"
            padding: "5dp"
            Spinner:
                id: addr_filter
                text: "{ar('اختر الحي / العنوان')}"
                values: []
                on_text: root.load_data(search_input.text)

        TextInput:
            id: search_input
            hint_text: "{ar('🔍 ابحث بالاسم...')}"
            size_hint_y: None
            height: "60dp"
            multiline: False
            halign: 'right'
            on_text: root.load_data(self.text)

        RecycleView:
            id: rv_list
            viewclass: 'BeneficiaryButton'
            RecycleBoxLayout:
                default_size: None, dp(80)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                spacing: "8dp"
                padding: "10dp"
        
        Button:
            text: "{ar('📊 استخراج النتائج التفصيلية (Excel)')}"
            size_hint_y: None
            height: "65dp"
            background_color: 0.1, 0.4, 0.1, 1
            on_release: app.export_to_excel()

<SurveyScreen>:
    name: 'survey'
    BoxLayout:
        orientation: 'vertical'
        padding: "10dp"
        spacing: "5dp"
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        Label:
            id: info_label
            color: 0.1, 0.3, 0.5, 1
            size_hint_y: None
            height: "45dp"
            font_size: '18sp'
            bold: True

        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: "15dp"

                Label:
                    text: "{ar('--- وضعية الربط بالشبكات ---')}"
                    color: 0.1, 0.5, 0.1, 1
                    size_hint_y: None
                    height: "30dp"
                
                GridLayout:
                    cols: 2
                    size_hint_y: None
                    height: "180dp"
                    spacing: "10dp"
                    CheckBox:
                        id: cb_elec
                    Label:
                        text: "{ar('الكهرباء')}"
                        color: 0,0,0,1
                    CheckBox:
                        id: cb_gas
                    Label:
                        text: "{ar('الغاز')}"
                        color: 0,0,0,1
                    CheckBox:
                        id: cb_water
                    Label:
                        text: "{ar('المياه')}"
                        color: 0,0,0,1
                    CheckBox:
                        id: cb_sanit
                    Label:
                        text: "{ar('التطهير')}"
                        color: 0,0,0,1

                Label:
                    text: "{ar('--- حالة البناية ---')}"
                    color: 0.1, 0.5, 0.1, 1
                    size_hint_y: None
                    height: "30dp"
                
                GridLayout:
                    cols: 2
                    size_hint_y: None
                    height: "220dp"
                    spacing: "10dp"
                    CheckBox:
                        id: st_1
                        group: 'status'
                    Label:
                        text: "{ar('في طور الانجاز')}"
                        color: 0,0,0,1
                    CheckBox:
                        id: st_2
                        group: 'status'
                    Label:
                        text: "{ar('على مستوى الاعمدة')}"
                        color: 0,0,0,1
                    CheckBox:
                        id: st_3
                        group: 'status'
                    Label:
                        text: "{ar('منتهية غير مشغولة')}"
                        color: 0,0,0,1
                    CheckBox:
                        id: st_4
                        group: 'status'
                    Label:
                        text: "{ar('منتهية ومشغولة')}"
                        color: 0,0,0,1

                Button:
                    text: "{ar('📸 التقاط صورة المسكن')}"
                    size_hint_y: None
                    height: "55dp"
                    on_release: root.open_camera()

                BoxLayout:
                    size_hint_y: None
                    height: "65dp"
                    spacing: "10dp"
                    Button:
                        text: "{ar('رجوع')}"
                        on_release: app.root.current = 'search'
                    Button:
                        text: "{ar('حفظ البيانات')}"
                        background_color: 0.1, 0.2, 0.3, 1
                        on_release: root.save_data()
"""

class SearchScreen(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(lambda dt: self.update_address_spinner(), 0.1)
        Clock.schedule_once(lambda dt: self.load_data(), 0.3)

    def update_address_spinner(self):
        try:
            conn = sqlite3.connect(App.get_running_app().db_path)
            c = conn.cursor()
            c.execute("SELECT DISTINCT address FROM beneficiaries")
            addrs = [str(row[0]).strip() for row in c.fetchall() if row[0]]
            conn.close()
            self.ids.addr_filter.values = [ar(a) for a in addrs] + [ar("الكل")]
        except: pass

    def load_data(self, query=""):
        if 'rv_list' not in self.ids: return
        try:
            conn = sqlite3.connect(App.get_running_app().db_path)
            sel_addr = self.ids.addr_filter.text
            df = pd.read_sql_query("SELECT id, name, program, address FROM beneficiaries WHERE completed=0", conn)
            conn.close()
            if sel_addr != ar("الكل") and sel_addr != ar("اختر الحي / العنوان"):
                df = df[df['address'].apply(lambda x: ar(str(x).strip()) == sel_addr)]
            if query:
                df = df[df['name'].str.contains(query, na=False)]
            
            self.ids.rv_list.data = [
                {'text': ar(f"{row['name']} | {row['program']}"), 
                 'on_release': lambda r=row: self.go_to_survey(r)} 
                for _, row in df.iterrows()
            ]
        except: pass

    def go_to_survey(self, row):
        s = self.manager.get_screen('survey')
        s.load_form(row['id'], row['name'])
        self.manager.current = 'survey'

class SurveyScreen(Screen):
    def load_form(self, uid, name):
        self.bid = uid
        self.ids.info_label.text = ar(f"المستفيد: {name}")
        for i in ['cb_elec','cb_gas','cb_water','cb_sanit','st_1','st_2','st_3','st_4']:
            self.ids[i].active = False

    def open_camera(self):
        # حفظ الصورة في المجلد الخاص بالتطبيق لضمان الصلاحيات
        fpath = os.path.join(App.get_running_app().user_data_dir, f"img_{self.bid}.jpg")
        try:
            camera.take_picture(filename=fpath, on_complete=lambda p: print(f"Saved: {p}"))
        except:
            print("خطأ في الكاميرا: يرجى التحقق من الصلاحيات")

    def save_data(self):
        status_txt = ""
        if self.ids.st_1.active: status_txt = "في طور الانجاز"
        elif self.ids.st_2.active: status_txt = "على مستوى الاعمدة"
        elif self.ids.st_3.active: status_txt = "منتهية غير مشغولة"
        elif self.ids.st_4.active: status_txt = "منتهية ومشغولة"

        try:
            conn = sqlite3.connect(App.get_running_app().db_path)
            c = conn.cursor()
            c.execute("UPDATE beneficiaries SET completed=1, status=?, elec=?, gas=?, water=?, sanit=? WHERE id=?",
                     (status_txt, int(self.ids.cb_elec.active), int(self.ids.cb_gas.active),
                      int(self.ids.cb_water.active), int(self.ids.cb_sanit.active), self.bid))
            conn.commit()
            conn.close()
            self.manager.current = 'search'
        except: pass

class MainApp(App):
    def build(self):
        # تحديد مسار قاعدة البيانات الآمن في أندرويد
        self.db_path = os.path.join(self.user_data_dir, 'census_2026.db')
        self.init_db()
        return Builder.load_string(KV)

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS beneficiaries 
                     (id INTEGER PRIMARY KEY, program TEXT, name TEXT, address TEXT,
                      elec INTEGER, gas INTEGER, water INTEGER, sanit INTEGER,
                      status TEXT, gps TEXT, completed INTEGER DEFAULT 0)''')
        conn.commit()
        conn.close()

    def import_new_data(self):
        try:
            filechooser.open_file(on_selection=self._on_file_selected)
        except: pass

    def _on_file_selected(self, selection):
        if not selection: return
        file_path = selection[0]
        try:
            if file_path.endswith('.xlsx'):
                df_new = pd.read_excel(file_path)
            else:
                df_new = pd.read_csv(file_path, encoding='utf-8', sep=None, engine='python')
            
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            for _, r in df_new.iterrows():
                # محاولة قراءة البيانات بمرونة
                prog, name, addr = str(r.iloc[1]), str(r.iloc[2]), str(r.iloc[4])
                c.execute("SELECT id FROM beneficiaries WHERE name=? AND program=?", (name, prog))
                if not c.fetchone():
                    c.execute("INSERT INTO beneficiaries (program, name, address) VALUES (?,?,?)", (prog, name, addr))
            conn.commit()
            conn.close()
            self.root.get_screen('search').update_address_spinner()
            self.root.get_screen('search').load_data()
        except Exception as e:
            print(f"Error Importing: {e}")

    def export_to_excel(self):
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT program, name, address, status, elec, gas, water, sanit FROM beneficiaries WHERE completed=1", conn)
            conn.close()
            if df.empty: return
            for col in ['elec', 'gas', 'water', 'sanit']:
                df[col] = df[col].apply(lambda x: 'X' if x == 1 else '')
            df.columns = ['البرنامج', 'الاسم', 'العنوان', 'الحالة', 'كهرباء', 'غاز', 'ماء', 'تطهير']
            # حفظ الملف في مجلد التحميلات العام إذا أمكن، أو مجلد التطبيق
            out_path = os.path.join(self.user_data_dir, "النتائج_التفصيلية.xlsx")
            df.to_excel(out_path, index=False)
        except: pass

    def export_stats(self):
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT program, status, elec, gas, water, sanit FROM beneficiaries WHERE completed=1", conn)
            df_quota = pd.read_sql_query("SELECT program, count(*) as quota FROM beneficiaries GROUP BY program", conn)
            conn.close()
            if df.empty: return
            
            df['s1'] = df['status'].apply(lambda x: 1 if x == "في طور الانجاز" else 0)
            df['s2'] = df['status'].apply(lambda x: 1 if x == "على مستوى الاعمدة" else 0)
            df['s3'] = df['status'].apply(lambda x: 1 if x == "منتهية غير مشغولة" else 0)
            df['s4'] = df['status'].apply(lambda x: 1 if x == "منتهية ومشغولة" else 0)
            
            summary = df.groupby('program').agg({
                's1': 'sum', 's2': 'sum', 's3': 'sum', 's4': 'sum',
                'elec': 'sum', 'gas': 'sum', 'water': 'sum', 'sanit': 'sum'
            }).reset_index()
            
            final = pd.merge(df_quota, summary, on='program', how='left').fillna(0)
            final.columns = ['البرنامج', 'حصة البرنامج', 'في طور الانجاز', 'على مستوى الأعمدة', 
                            'منتهية غير مشغولة', 'منتهية ومشغولة', 'الكهرباء', 'الغاز', 'المياه', 'التطهير']
            
            out_path = os.path.join(self.user_data_dir, "الجدول_الإحصائي_الإجمالي.xlsx")
            final.to_excel(out_path, index=False)
        except: pass

if __name__ == '__main__':
    MainApp().run()
