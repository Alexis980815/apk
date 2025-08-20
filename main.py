from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from collections import defaultdict


class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.total_limpio = 0.0
        self.fijos_data = {}
        self.parles_data = {}
        self.centenas_data = {}

        self.ids.fijos_num.bind(text=self.check_fijos_input)
        self.ids.parles_num.bind(text=self.check_parles_input)
        self.ids.centenas_num.bind(text=self.check_centenas_input)

    def show_totals(self):
        combined_data = defaultdict(float)

        # Sumar los fijos
        for num, amount in self.fijos_data.items():
            combined_data[num] += amount

        # Sumar los centenas
        for num, amount in self.centenas_data.items():
            combined_data[num] += amount

        # Procesar parles_data para agrupar números por importe
        parles_totals = defaultdict(list)
        for num in self.parles_data:
            importe = self.parles_data[num]
            parles_totals[importe].append(num)

        popup = TotalTablePopup(combined_data=combined_data, parles_data=parles_totals)
        popup.open()

    def check_fijos_input(self, instance, value):
        if len(value) == 2:
            self.ids.fijos_amount.focus = True

    def check_parles_input(self, instance, value):
        lines = value.splitlines()
        if lines and len(lines[-1]) == 2:
            if not value.endswith('\n'):
            	Clock.schedule_once(lambda dt: self.add_new_line_to_parles(instance), 0.1)

    def add_new_line_to_parles(self, instance):
        instance.text += '\n'
        instance.focus = True

    def check_centenas_input(self, instance, value):
        if len(value) == 2:
            self.ids.centenas_amount.focus = True

    def add_fijos(self):
        num = self.ids.fijos_num.text
        amount = self.ids.fijos_amount.text
        try:
            amount_float = float(amount)
            # Usar un diccionario para almacenar los datos
            self.fijos_data[num] = self.fijos_data.get(num, 0) + amount_float
            self.total_limpio += amount_float
            self.update_display()
            self.ids.fijos_num.text = ''
            self.ids.fijos_amount.text = ''
        except ValueError:
            pass

    def add_parles(self):
        num = self.ids.parles_num.text
        amount = self.ids.parles_amount.text
        try:
            amount_float = float(amount)
            self.parles_data[num] = self.parles_data.get(num, 0) + amount_float
            self.total_limpio += amount_float
            self.update_display()
            self.ids.parles_num.text = ''
            self.ids.parles_amount.text = ''
        except ValueError:
            pass

    def add_centenas(self):
        num = self.ids.centenas_num.text
        amount = self.ids.centenas_amount.text
        try:
            amount_float = float(amount)
            self.centenas_data[num] = self.centenas_data.get(num, 0) + amount_float
            self.total_limpio += amount_float
            self.update_display()
            self.ids.centenas_num.text = ''
            self.ids.centenas_amount.text = ''
        except ValueError:
            pass

    def clean_dates(self):
        self.total_limpio = 0.0
        self.fijos_data = {}
        self.parles_data = {}
        self.centenas_data = {}
        self.update_display()

    def update_display(self):
        self.ids.limpio_label.text = f'Limpio: {self.total_limpio:.2f}'
        # 1. Convertir los datos de los diccionarios a una lista de strings
        fijos_text = [f"{num}: ${amount:.2f}" for num, amount in self.fijos_data.items()]
        parles_text = [f"{num}: ${amount:.2f}" for num, amount in self.parles_data.items()]
        centenas_text = [f"{num}: ${amount:.2f}" for num, amount in self.centenas_data.items()]

        # 2. Unir las listas de strings para actualizar las etiquetas
        self.ids.fijos_list.text = '\n'.join(fijos_text)
        self.ids.parles_list.text = '\n'.join(parles_text)
        self.ids.centenas_list.text = '\n'.join(centenas_text)

class TotalTablePopup(Popup):
    def __init__(self, combined_data, parles_data, **kwargs):
        super(TotalTablePopup, self).__init__(**kwargs)
        self.title = 'Totales por número'
        self.size_hint = (0.9, 0.9)
        self.auto_dismiss = True

        main_layout = BoxLayout(orientation='vertical')

        scroll_view = ScrollView(do_scroll_x=False, do_scroll_y=True)
        table_layout = GridLayout(cols=2, spacing=5, size_hint_y=None)
        table_layout.bind(minimum_height=table_layout.setter('height'))

        # Encabezados
        table_layout.add_widget(Label(text='Número', bold=True, size_hint_y=None, height=30))
        table_layout.add_widget(Label(text='Total', bold=True, size_hint_y=None, height=30))

        # Sección de fijos y centenas
        try:
            sorted_keys = sorted(combined_data.keys(), key=int)
        except (ValueError, TypeError):
            sorted_keys = sorted(combined_data.keys())

        for num in sorted_keys:
            amount = combined_data[num]
            table_layout.add_widget(Label(text=str(num), halign='left', valign='middle', size_hint_y=None, height=30))
            table_layout.add_widget(Label(text=f'${amount:.2f}', halign='right', valign='middle', size_hint_y=None, height=30))

        # Espaciado entre secciones
        table_layout.add_widget(Label(size_hint_y=None, height=10))
        table_layout.add_widget(Label(size_hint_y=None, height=10))

        # Sección de Parles
        if parles_data:
            table_layout.add_widget(Label(text='Parles', bold=True, size_hint_y=None, height=30))
            table_layout.add_widget(Label(text='Importe', bold=True, size_hint_y=None, height=30))

        sorted_parles_amounts = sorted(parles_data.keys())
        for amount in sorted_parles_amounts:
            numbers = parles_data[amount]
            # Formato de guiones
            numbers_text = '-'.join(numbers)

            # Label que se ajusta a la altura del texto
            numbers_label = Label(text=numbers_text, halign='left', valign='middle', text_size=(table_layout.width / 2 - 10, None), size_hint_y=None)
            numbers_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

            # Label del importe
            amount_label = Label(text=f'${amount:.2f}', halign='right', valign='middle', size_hint_y=None, height=numbers_label.height)
            numbers_label.bind(height=lambda instance, value: setattr(amount_label, 'height', value))

            table_layout.add_widget(numbers_label)
            table_layout.add_widget(amount_label)

        scroll_view.add_widget(table_layout)
        main_layout.add_widget(scroll_view)

        close_button = Button(text='Cerrar', size_hint_y=None, height=40)
        close_button.bind(on_press=self.dismiss)
        main_layout.add_widget(close_button)

        self.content = main_layout

class BolitaApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#f0f0f0')
        Window.softinput_mode = 'below_target'
        return MainWidget()

if __name__ == '__main__':
    BolitaApp().run()