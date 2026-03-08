#!/usr/bin/env python3
import sys
from gen import *
from pprint import pprint


class CustomRow(Row):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill = Fill.X


class Window(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.view_layout = True

        # self.spacing = 6
        # lay = self.add(Row(margin=8, spacing=6))
        self.add(Empty(fill=Fill.X))
        self.add(Button('Button', fill=Fill.X))
        self.add(Input(fill=Fill.X))
        num = 1
        for x in range(5):
            row = self.add(CustomRow(margin=6, spacing=6))

            for y in range(5):
                style = None
                text = str(num)

                if   num == 16: style, text = StyleClass.DEFAULT, 'DEFAULT'
                elif num == 17: style, text = StyleClass.CHECKED, 'CHECKED'
                elif num == 18: style, text = StyleClass.DISABLED, 'DISABLED'
                elif num == 21: style, text = StyleClass.SUCCESS, 'SUCCESS'
                elif num == 22: style, text = StyleClass.WARNING, 'WARNING'
                elif num == 23: style, text = StyleClass.ERROR, 'ERROR'
                
                b = row.add(Button(text, style_class=style, elided=True))
                b.pressed.connect(self.on_pressed)
                b.min_width = 50

                if num == 25:
                    b.released.connect(lambda sender: print(sender, 'Exiting...'))
                    self.default = b
                num += 1
        
        r = self.add(Row(margin=6, spacing=6, fill=Fill.XY))
        ed = r.add(Empty(style_class=StyleClass.DEFAULT))
        es = r.add(Empty(style_class=StyleClass.SUCCESS))
        ee = r.add(Empty(style_class=StyleClass.ERROR))
        ew = r.add(Empty(style_class=StyleClass.WARNING))

        self.btn = self.add(Button('Click me!'))
        # self.add(Timer(interval=0.5, call=lambda: print('CALL')))

        for ui in (ed, es, ee, ew, self.btn):
            ui.enter.connect(self.on_enter)
            ui.pressed.connect(self.on_pressed)
            ui.released.connect(self.on_released)
            ui.right_pressed.connect(
                lambda sender: self.on_pressed(sender, 'RIGHT_'))
            ui.right_released.connect(
                lambda sender: self.on_released(sender, 'RIGHT_'))
            
            ui.accept_move = True
            ui.move.connect(self.on_move)
            
            ui.leave.connect(self.on_leave)

            ui.drag_start.connect(
                lambda sender: self.on_drag(sender, 'DRAG_START'))
            ui.drag_end.connect(
                lambda sender: self.on_drag(sender, 'DRAG_END'))
    
    def on_enter(self, sender):
        print(sender, 'ENTER')
    
    def on_pressed(self, sender, side: str = ''):
        print(sender, side + 'PRESSED')
    
    def on_released(self, sender, side: str = ''):
        print(sender, side + 'RELEASED')
    
    def on_leave(self, sender):
        print(sender, 'LEAVE')
    
    def on_move(self, sender):
        print(sender, 'MOVE, dragging:', sender.dragging)
    
    def on_drag(self, sender, var):
        print(sender, var)


if __name__ == '__main__':
    app = Application(Window)
    app.size = 600, 400
    app.name = 'App'
    app.title = 'My App'
    sys.exit(app.run())
