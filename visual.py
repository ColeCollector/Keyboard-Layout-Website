from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import RoundedRectangle, Color, Rectangle
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from _main import evaluate

Window.size = (800, 800)

# Add whatever you want in here
layouts = [['qpdmxzyou;', 'rnthfgsaei', 'wbkljvc,.?'], 
           ['qwertyuiop', 'asdfghjkl;', 'zxcvbnm,.?'],
           ['gvdfjqruo;', 'csthyxneai', 'wbmpkzl,.?'],
           ['bldwz;fouj', 'nrtsgyhaei', 'qxmcvkp,.?']]

class KeyboardWidget(Widget):
    def __init__(self, layouts,  **kwargs):  # Accept layout as a parameter
        super().__init__(**kwargs)
        with self.canvas:
            # Draw background
            Color(0.15, 0.15, 0.28, 1)
            self.bg = Rectangle(size=(800, 800), pos=self.pos)

        self.evaluations =[{} for _ in range(len(layouts))]
        self.widgets = []
        self.selected = 0
        self.layouts = layouts
        self.create_grid()
        self.create_keyboard()
        
        self.default_text = "Choose a corpus"

        arrow1 = Button(
            pos=(740, 520),
            text=">",
            background_color=(0.19, 0.19, 0.34, 1),
            size_hint=(None, None),
            size=(50, 100))
        

        arrow2 = Button(
            pos=(10, 520),
            text="<",
            background_color=(0.19, 0.19, 0.34, 1),
            size_hint=(None, None),
            size=(50, 100))

        arrow1.bind(on_release=lambda instance: self.switch(1))
        self.add_widget(arrow1)

        arrow2.bind(on_release=lambda instance: self.switch(-1))
        self.add_widget(arrow2)
        self.dropdown_button()

    def dropdown_button(self):
        # Create the dropdown
        dropdown = DropDown()

        # Add items to the dropdown
        options = ["Discord", "English-1k", "English-200", "Keymash", "Monkey-Type", "My_Discord"]
        for option in options:
            # Create a button for each option
            btn = Button(
                text=option,
                size_hint_y=None,
                height=44,
                background_color=(0.19, 0.19, 0.34, 1),
            )
            # Bind the button to update the main button's text and close the dropdown
            btn.bind(on_release=lambda btn: self.on_option_selected(btn, dropdown, main_button))
            dropdown.add_widget(btn)

        # Create the main button to trigger the dropdown
        
        main_button = Button(
            pos=(530, 360),
            text=self.default_text,
            background_color=(0.19, 0.19, 0.34, 1),
            size_hint=(None, None),
            size=(200, 50))

        # Bind the main button to open the dropdown
        main_button.bind(on_release=dropdown.open)
        self.widgets.append(main_button)
        self.add_widget(main_button)

    def switch(self, direction):
        if direction == 1:
            self.selected = self.selected + direction if self.selected != len(self.layouts) - 1 else 0
        elif direction == -1:
            self.selected = self.selected + direction if self.selected != 0 else len(self.layouts) - 1

        # Update the keyboard
        self.create_keyboard()
        self.dropdown_button()

        # Update the stats after arrow is used
        if self.default_text != "Choose a corpus":
            self.update_text(self.default_text)

    def update_text(self, corpus):

        if corpus not in self.evaluations[self.selected]:
            evaluation = evaluate([self.layouts[self.selected]], corpus)
            self.evaluations[self.selected][corpus] = evaluation
        else:
            evaluation = self.evaluations[self.selected][corpus]

        self.stats = evaluation[0]
        self.weights = evaluation[1]
        self.corpus_count = evaluation[2]
        #print(self.corpus_count)
        self.movement = evaluation[3]
        self.text_chunk = (
            f"[color=6E6ECC]SFB         : {self.cleanup('SFB')} | {self.cleanup('BadSfb')}\n"
            f"SFS         : {self.cleanup('SFS')} | {self.cleanup('BadSfs')}\n"
            f"Scissors    : {self.cleanup('Scissors')} | {self.cleanup('BadScis')}\n\n"
            f"Redirects   : {self.cleanup('Redirects')} | {self.cleanup('BadRed')}\n"
            f"Inrolls     : {self.cleanup('Inrolls')} | {self.cleanup('Trinroll')}\n"
            f"Outrolls    : {self.cleanup('Outrolls')} | {self.cleanup('Trioutroll')}\n"
            f"Alt         : {self.cleanup('Alt')}\n"
            f"LSB         : {self.cleanup('LSB')}\n"
            f"Score       : {round(100 - 8 * self.movement/self.corpus_count, 1)} / 100[/color]")

        self.stats_label.text = self.text_chunk

    def colorize_string(self, string):
        charcount = {'e': 51322, 't': 37436, 'o': 33403, 'a': 31347, 'n': 28696, 'i': 26107, 's': 25097, 'r': 23278, 'h': 22707, 'l': 17690, 'd': 15355, 'u': 13650, 'm': 10520, 'y': 10236, 'c': 9657, 'w': 9313, 'g': 9097, 'f': 8662, '.': 6782, 'p': 6780, ',': 6332, 'b': 6086, 'v': 4325, 'k': 3897, '?': 565, 'x': 550, 'j': 545, 'q': 359, 'z': 305, ';': 163}
        number = 0.017*charcount[string]/1000
        pct_diff = 1.0 - number
        b = round(min(255, pct_diff* 255))
        r = round(min(255, (number*0.25) * 10 * 255))
        return r/255, 0, b/255, 1

    def cleanup(self, stat):
        value = (self.stats[stat]*self.weights[stat])/self.corpus_count
        if value < 0: value = 0.3 + value
        value = max(0, min(0.2, value)) / 0.2

        red = int(255 * value)
        green = int(255 * (1 - value))
        return f"[color={red:02x}{green:02x}00]{round(self.stats[stat]*100/self.corpus_count, 1)}%[/color]"
    
    def on_option_selected(self, btn, dropdown, main_button):
        """
        Callback for when an option is selected.
        Updates the main button's text and closes the dropdown.
        """
        main_button.text = btn.text  # Updates the main button text
        self.default_text = btn.text
        self.update_text(btn.text)
        dropdown.dismiss()  # Close the dropdown

    def create_keyboard(self):
        rows, cols = 3, 10
        square_size = 50  # Size of each key
        spacing = 10  # Space between keys
        for key in self.widgets:
            self.remove_widget(key)
            
        with self.canvas:
            # Keyboard Keys
            for row in range(rows):
                for col in range(cols):
                    x = col * (square_size + spacing) + 95
                    y = 600 - row * (square_size + spacing) 
                    if col > 4: x += 20

                    # Draw the key
                    Color(*self.colorize_string(self.layouts[self.selected][row][col]))
                    RoundedRectangle(
                        pos=(x, y),
                        size=(square_size, square_size),
                        radius=[(13, 13) * 4])

                    # Draw the letter
                    key = (Label(
                        text=f"{self.layouts[self.selected][row][col].upper()}",
                        font_size=25,
                        color=(0, 0, 0, 1),  # Black color
                        size_hint=(None, None),
                        size=(square_size, square_size),
                        pos=(x, y)))
                    self.widgets.append(key)
                    self.add_widget(key)
                    
    def create_grid(self):
        # Create the UI
        with self.canvas:
            # Aesthetic Rectangles
            Color(0.22, 0.22, 0.42, 1)
            RoundedRectangle(
                pos=(71, 451),
                size=(658, 228),
                radius=[(15, 15) * 4])

            Color(0.19, 0.19, 0.34, 1)
            RoundedRectangle(
                pos=(75, 455),
                size=(650, 220),
                radius=[(10, 10) * 4])

            RoundedRectangle(
                pos=(75, 25),
                size=(430, 390),
                radius=[(10, 10) * 4])
                    
        # Create and manually position title text
        self.stats_label = Label(
            text= "[color=6E6ECC]Nothing to display[/color]",
            font_size=25,
            font_name="RobotoMono-Regular",
            size_hint=(None, None),
            size=(300, 50),
            pos=(140, 200),
            markup=True)
        self.add_widget(self.stats_label)

        self.title = Label(
            text= f"[color=6E6ECC]KEYBOARD ANALYZER[/color]",
            font_size=35,
            font_name="RobotoMono-Regular",
            size_hint=(None, None),
            size=(800, 50),
            pos=(0, 705),
            markup=True)
        self.add_widget(self.title)

class KeyboardApp(App):
    def __init__(self, layouts, **kwargs):
        super().__init__(**kwargs)
        self.layouts = layouts

    def build(self):
        return KeyboardWidget(layouts=self.layouts)
    
if __name__ == '__main__':
    KeyboardApp(layouts).run()


    