from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
import arabic_reshaper
from bidi.algorithm import get_display

# النصوص باللغتين
translations = {
    "en": {
        "header": "Tech Development Department - East Fayoum",
        "overview": "Overview",
        "projects": "Projects and Activities",
        "news": "News and Announcements",
        "resources": "Resource Library",
        "popup_overview": "The Tech Development Department focuses on enhancing technical skills and improving infrastructure.",
        "popup_projects": "Our activities include workshops, seminars, and ongoing development projects.",
        "popup_news": "Stay updated with the latest news and announcements from the department.",
        "popup_resources": "The resource library offers access to educational materials, videos, and e-books.",
        "contact_popup": "Contact Us",
        "phone_number": "Phone: 01062045083",
        "message": "Message"
    },
    "ar": {
        "header": "قسم التطوير التكنولوجي - شرق الفيوم",
        "overview": "لمحة عامة",
        "projects": "المشاريع والأنشطة",
        "news": "الأخبار والإعلانات",
        "resources": "مكتبة الموارد",
        "popup_overview": "يركز قسم التطوير التكنولوجي على تعزيز المهارات التقنية وتحسين البنية التحتية.",
        "popup_projects": "تشمل أنشطتنا ورش العمل والندوات والمشاريع التطويرية الجارية.",
        "popup_news": "ابقَ محدثًا مع أحدث الأخبار والإعلانات من القسم.",
        "popup_resources": "توفر مكتبة الموارد الوصول إلى المواد التعليمية والفيديوهات والكتب الإلكترونية.",
        "contact_popup": "تواصل معنا",
        "phone_number": "الهاتف: 01062045083",
        "message": "الرسالة"
    }
}

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = "en"  # اللغة الافتراضية هي الإنجليزية
        self.button_layout = None  # لتخزين ترتيب الأزرار لاستخدامه عند التغيير

    def build(self):
        # إعداد الواجهة
        layout = FloatLayout(size=(Window.width, Window.height))

        # إضافة الخلفية
        background_image = Image(source="1.jpg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(background_image)

        # إضافة عنوان التطبيق
        self.header = Label(
            text=self.get_text("header"),
            font_size=22,
            size_hint=(0.9, None),
            height=50,
            pos_hint={"x": 0.05, "top": 0.95},
            color=(1, 1, 1, 1),
            bold=True
        )
        layout.add_widget(self.header)

        # إضافة الأزرار
        self.button_layout = BoxLayout(orientation="vertical", padding=10, spacing=10, size_hint=(0.8, 0.5), pos_hint={"x": 0.1, "y": 0.2})
        self.create_buttons()
        layout.add_widget(self.button_layout)

        # إضافة قائمة لاختيار اللغة
        dropdown = DropDown()
        languages = ["en", "ar"]
        for lang in languages:
            btn = Button(text=lang.upper(), size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.change_language(btn.text.lower(), dropdown))
            dropdown.add_widget(btn)

        # زر اختيار اللغة
        language_button = Button(
            text="Change Language",
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={"right": 0.95, "bottom": 0.05},  # تحديد موقع الزر في أسفل اليمين
            background_color=(0.1, 0.6, 1, 1),  # لون الزر
            color=(1, 1, 1, 1)  # لون النص
        )
        language_button.bind(on_release=dropdown.open)
        layout.add_widget(language_button)

        # إضافة زر "تواصل معنا"
        contact_button = Button(
            text=self.get_text("contact_popup"),
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"left": 0.05, "bottom": 0.05},
            background_color=(0.1, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size=18
        )
        contact_button.bind(on_press=self.show_contact_popup)
        layout.add_widget(contact_button)

        return layout

    def create_buttons(self):
        self.button_layout.clear_widgets()
        buttons = [
            (self.get_text("overview"), self.show_overview),
            (self.get_text("projects"), self.show_projects),
            (self.get_text("news"), self.show_news),
            (self.get_text("resources"), self.show_resources)
        ]

        for text, callback in buttons:
            btn = Button(
                text=text, 
                size_hint=(1, None), 
                height=50, 
                background_color=(0.1, 0.6, 1, 1),  # Light blue color
                color=(1, 1, 1, 1),  # White text color
                font_size=18
            )
            btn.bind(on_press=callback)
            self.button_layout.add_widget(btn)

    def change_language(self, lang, dropdown):
        self.language = lang
        dropdown.dismiss()
        self.update_labels()

    def update_labels(self):
        # تحديث النصوص بناءً على اللغة
        self.header.text = self.get_text("header")
        self.create_buttons()  # إعادة إنشاء الأزرار مع النصوص الجديدة

    def get_text(self, key):
        text = translations[self.language][key]
        if self.language == "ar":
            reshaped_text = arabic_reshaper.reshape(text)
            return get_display(reshaped_text)
        return text

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()

    def show_contact_popup(self, instance):
        # إنشاء نافذة "تواصل معنا"
        contact_layout = BoxLayout(orientation="vertical", padding=10)
        
        # إضافة رقم الهاتف
        phone_label = Label(text=self.get_text("phone_number"), font_size=18, size_hint_y=None, height=40)
        contact_layout.add_widget(phone_label)

        # إضافة حقل النص لكتابة الرسالة
        message_label = Label(text=self.get_text("message"), font_size=18, size_hint_y=None, height=40)
        contact_layout.add_widget(message_label)

        message_input = TextInput(hint_text="Type your message here...", size_hint_y=None, height=150, font_size=16)
        contact_layout.add_widget(message_input)

        # زر إرسال
        send_button = Button(text="Send", size_hint_y=None, height=50, background_color=(0.1, 0.6, 1, 1), color=(1, 1, 1, 1))
        send_button.bind(on_press=lambda btn: self.send_message(message_input.text, send_button))
        contact_layout.add_widget(send_button)

        # عرض النافذة
        popup = Popup(
            title=self.get_text("contact_popup"),
            content=contact_layout,
            size_hint=(0.8, 0.8)
        )
        popup.open()

    def send_message(self, message, send_button):
        # هنا يمكن إرسال الرسالة إلى البريد الإلكتروني أو قاعدة البيانات
        print(f"Message sent: {message}")
        # إغلاق النافذة بعد الإرسال
        send_button.parent.dismiss()

    def show_overview(self, instance):
        self.show_popup("Overview", self.get_text("popup_overview"))

    def show_projects(self, instance):
        self.show_popup("Projects and Activities", self.get_text("popup_projects"))

    def show_news(self, instance):
        self.show_popup("News and Announcements", self.get_text("popup_news"))

    def show_resources(self, instance):
        self.show_popup("Resource Library", self.get_text("popup_resources"))

if __name__ == "__main__":
    MainApp().run()
