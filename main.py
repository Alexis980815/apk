# file: main.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class BolitaApp(App):
    def build(self):
        # Configurar el color de fondo general
        Window.clearcolor = get_color_from_hex('#f0f0f0')
        
        # Variables para almacenar los datos
        self.total_limpio = 0.0
        self.fijos_data = []
        self.parles_data = []
        self.centenas_data = []
        
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Encabezado
        self.header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.title_label = Label(text='Florida', font_size=20, halign='left', size_hint=(0.7, 1))
        self.limpio_label = Label(text=f'Limpio: {self.total_limpio:.2f}', font_size=20, halign='right', size_hint=(0.3, 1))
        
        self.footer = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        
        self.header.add_widget(self.title_label)
        self.header.add_widget(self.limpio_label)
        main_layout.add_widget(self.header)
        
        
        
        # Tabla
        table = GridLayout(cols=3, rows=1, spacing=5, size_hint=(1, 0.9))
        
        # === Columna Fijos y Corridos (Orden corregido) ===
        self.column1 = BoxLayout(orientation='vertical', spacing=5)
        self.column1.add_widget(Label(text='Fijos', font_size=15, bold=True, size_hint=(1, 0.1)))
        
        # 1. Añade la lista primero (la "tabla")
        self.fijos_list = Label(text='', size_hint=(1, 0.7))
        self.column1.add_widget(self.fijos_list)

        # 2. Luego los campos de entrada
        fijos_input = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.fijos_num = TextInput(hint_text='#__', multiline=False, size_hint=(0.5, 1))
        self.fijos_amount = TextInput(hint_text='$__', multiline=False, size_hint=(0.5, 1))
        fijos_input.add_widget(self.fijos_num)
        fijos_input.add_widget(self.fijos_amount)
        self.column1.add_widget(fijos_input)
        
        # 3. Finalmente el botón
        fijos_btn = Button(text='Agregar', size_hint=(1, 0.1))
        fijos_btn.bind(on_press=self.add_fijos)
        self.column1.add_widget(fijos_btn)
        
        # === Columna Parles (Orden corregido) ===
        self.column2 = BoxLayout(orientation='vertical', spacing=5)
        self.column2.add_widget(Label(text='Parles', font_size=15, bold=True, size_hint=(1, 0.1)))
        
        # 1. Añade la lista primero
        self.parles_list = Label(text='', size_hint=(1, 0.7))
        self.column2.add_widget(self.parles_list)
        
        # 2. Luego los campos de entrada
        parles_input = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.parles_num = TextInput(hint_text='#__', multiline=False, size_hint=(0.5, 1))
        self.parles_amount = TextInput(hint_text='$__', multiline=False, size_hint=(0.5, 1))
        parles_input.add_widget(self.parles_num)
        parles_input.add_widget(self.parles_amount)
        self.column2.add_widget(parles_input)
        
        # 3. Finalmente el botón
        parles_btn = Button(text='Agregar', size_hint=(1, 0.1))
        parles_btn.bind(on_press=self.add_parles)
        self.column2.add_widget(parles_btn)
        
        # === Columna Centenas (Orden corregido) ===
        self.column3 = BoxLayout(orientation='vertical', spacing=5)
        self.column3.add_widget(Label(text='Corridos', font_size=15, bold=True,size_hint=(1, 0.1)))
        
        # 1. Añade la lista primero
        self.centenas_list = Label(text='', size_hint=(1, 0.7))
        self.column3.add_widget(self.centenas_list)
        
        # 2. Luego los campos de entrada
        centenas_input = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.centenas_num = TextInput(hint_text='#__', multiline=False, size_hint=(0.5, 1))
        self.centenas_amount = TextInput(hint_text='$__', multiline=False, size_hint=(0.5, 1))
        centenas_input.add_widget(self.centenas_num)
        centenas_input.add_widget(self.centenas_amount)
        self.column3.add_widget(centenas_input)
        
        # 3. Finalmente el botón
        centenas_btn = Button(text='Agregar', size_hint=(1, 0.1))
        centenas_btn.bind(on_press=self.add_centenas)
        self.column3.add_widget(centenas_btn)
        
        #4. Boton para reiniciar
        clean_btn = Button(text='Eliminar Todo', size_hint=(1, 0.1))
        clean_btn.bind(on_press=self.clean_dates)
        self.footer.add_widget(clean_btn)

        table.add_widget(self.column1)
        table.add_widget(self.column2)
        table.add_widget(self.column3)
        
        main_layout.add_widget(table)
        main_layout.add_widget(self.footer)
        
        return main_layout
    
    def add_fijos(self, instance):
        num = self.fijos_num.text
        amount = self.fijos_amount.text
        try:
            amount_float = float(amount)
            self.fijos_data.append((num, amount_float))
            self.total_limpio += amount_float
            self.update_display()
            self.fijos_num.text = ''
            self.fijos_amount.text = ''
        except ValueError:
            pass
    
    def add_parles(self, instance):
        num = self.parles_num.text
        amount = self.parles_amount.text
        try:
            amount_float = float(amount)
            self.parles_data.append((num, amount_float))
            self.total_limpio += amount_float
            self.update_display()
            self.parles_num.text = ''
            self.parles_amount.text = ''
        except ValueError:
            pass
    
    def add_centenas(self, instance):
        num = self.centenas_num.text
        amount = self.centenas_amount.text
        try:
            amount_float = float(amount)
            self.centenas_data.append((num, amount_float))
            self.total_limpio += amount_float
            self.update_display()
            self.centenas_num.text = ''
            self.centenas_amount.text = ''
        except ValueError:
            pass
    
    def clean_dates(self, instance):
        self.total_limpio = 0.0
        self.fijos_data = []
        self.parles_data = []
        self.centenas_data = []
        self.update_display()
    
    def update_display(self):
        # Actualizar el total limpio
        self.limpio_label.text = f'Limpio: {self.total_limpio:.2f}'
        
        # Actualizar las listas
        self.fijos_list.text = '\n'.join([f"{num}: ${amount:.2f}" for num, amount in self.fijos_data])
        self.parles_list.text = '\n'.join([f"{num}: ${amount:.2f}" for num, amount in self.parles_data])
        self.centenas_list.text = '\n'.join([f"{num}: ${amount:.2f}" for num, amount in self.centenas_data])

if __name__ == '__main__':
    BolitaApp().run()