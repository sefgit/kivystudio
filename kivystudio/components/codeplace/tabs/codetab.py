from kivy.uix.behaviors import ToggleButtonBehavior,ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy.properties import (StringProperty,
                            ObjectProperty,
                            BooleanProperty)
from kivystudio.behaviors import HoverInfoBehavior
from kivystudio.behaviors import HighlightBehavior
from kivystudio.widgets.iconlabel import IconLabelButton
from kivystudio.widgets.rightclick_drop import RightClickDrop
from kivystudio.tools import set_auto_mouse_position
from kivystudio.tools.iconfonts import icon
from kivystudio.components.emulator_area import get_emulator_area

rightclick_dropdown = [None]

class TabToggleButton(HoverInfoBehavior, ToggleButtonBehavior, BoxLayout):

    filename = StringProperty('')

    saved = BooleanProperty(True)

    text = StringProperty('')

    def __init__(self, **kwargs):
        super(TabToggleButton, self).__init__(**kwargs)
        # set the info attr because filename could change
        self.info_text_attr = 'filename'

        if rightclick_dropdown[0] is None:
            self.rightclick_dropdown = CodeTabDropDown()
            rightclick_dropdown[0] = self.rightclick_dropdown
        else:
            self.rightclick_dropdown=rightclick_dropdown[0]

    def on_saved(self, *args):
        if self.saved:
            self.ids.indicator.text =''
        elif not self.saved:
            self.ids.indicator.text = '%s' % (icon('fa-circle'))
            self.ids.indicator.font_size = '12dp'

    def on_state(self, *args):
        if self.state=='down' and not self.saved:
            self.ids.indicator.text = '%s' % (icon('fa-circle'))
            self.ids.indicator.font_size = '12dp'
        elif self.state=='down' and self.saved:
            self.ids.indicator.text = '%s' % (icon('fa-close'))
            self.ids.indicator.font_size = '16dp'
        elif self.state=='normal':
            self.ids.indicator.source =''
 

    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'right':
                self.rightclick_dropdown.open(self)
                FocusBehavior.ignored_touch.append(touch)
                return True

        if touch.button == 'left':
            return super(TabToggleButton, self).on_touch_down(touch)

    def close_tab(self):
        from kivystudio.assembler import code_place
        code_place.remove_code_tab(self)


    def __str__(self):
        return self.filename


class CodeTabDropDown(RightClickDrop):

    def __init__(self, **kwargs):
        super(CodeTabDropDown, self).__init__(**kwargs)
        self.tab = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):  # touch should not unfocus input
            FocusBehavior.ignored_touch.append(touch)
        return super(CodeTabDropDown,self).on_touch_down(touch)

    def open(self, tab):
        self.tab=tab
        super(CodeTabDropDown, self).open()

    def set_for_emulation(self, remove=False):
        if not remove:
            get_emulator_area().emulation_file=self.tab.filename
        else:
            get_emulator_area().emulation_file=''

    def close_tab(self):
        self.dismiss()
        self.tab.close_tab()


class TabPannelIndicator(IconLabelButton):
        
    def on_hover(self, *a):
        if self.hover:
            self.text = '%s' % (icon('fa-close'))
            self.font_size = '16dp'
        if not self.hover and not self.parent.saved:
            self.text = '%s' % (icon('fa-circle'))
            self.font_size = '12dp'
        if not self.hover and self.parent.saved and self.parent.state=='normal':
            self.text = ''
        if not self.hover and self.parent.saved and self.parent.state=='down':
            self.text = '%s' % (icon('fa-close'))
            self.font_size = '16dp'

        return super(TabPannelIndicator, self).on_hover(*a)
