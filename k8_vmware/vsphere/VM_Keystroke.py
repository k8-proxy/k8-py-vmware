import pyVmomi


class VM_Keystroke:

    def __init__(self, vm):
        self.vm = vm

    def convert_key_to_HID(self, char):
        for key, code, values in HIDCode:
            if char == key:
                key, modifiers = values[0]
                return code, modifiers

    def convert_char_to_HID(self, char):
        for key, code, values in HIDCode:
            for key, modifiers in values:
                if char == key:
                    return code, modifiers

    def HID2HEX(self, hid):
        return (int(hid, 16) << 16 | 0o0007)

    def send_key_stoke(self, code, modifiers):     # todo: refactor code (currently based on code from https://github.com/at-ohms/VMKey/blob/master/VMKey.py)
        tmp = pyVmomi.vim.UsbScanCodeSpecKeyEvent()
        m = pyVmomi.vim.UsbScanCodeSpecModifierType()
        if "KEY_LEFTSHIFT" in modifiers:
            m.leftShift = True
        if "KEY_RIGHTALT" in modifiers:
            m.rightAlt = True
        if "CTRL" in modifiers:
            m.leftControl = True
        if "ALT" in modifiers:
            m.leftAlt = True
        tmp.modifiers = m
        tmp.usbHidCode = self.HID2HEX(code)
        sp = pyVmomi.vim.UsbScanCodeSpec()
        sp.keyEvents = [tmp]
        return self.vm.vm.PutUsbScanCodes(sp)

    def send_char(self, char):
        code, modifiers = self.convert_char_to_HID(char)
        self.send_key_stoke(code, modifiers)

    def send_key(self, key):
        code, modifiers  = self.convert_key_to_HID(key)
        return self.send_key_stoke(code, modifiers)

    def send_text(self, text):
        for char in list(text):
            self.send_char(char)
        return self

    # key helpers
    def enter(self): self.send_key("KEY_ENTER") ; return self
    def esc  (self): self.send_key("KEY_ESC"  ) ; return self

HIDCode = [
        ('KEY_A', '0x04', [('a', []), ('A', ['KEY_LEFTSHIFT'])]),
        ('KEY_B', '0x05', [('b', []), ('B', ['KEY_LEFTSHIFT'])]),
        ('KEY_C', '0x06', [('c', []), ('C', ['KEY_LEFTSHIFT'])]),
        ('KEY_D', '0x07', [('d', []), ('D', ['KEY_LEFTSHIFT'])]),
        ('KEY_E', '0x08', [('e', []), ('E', ['KEY_LEFTSHIFT'])]),
        ('KEY_F', '0x09', [('f', []), ('F', ['KEY_LEFTSHIFT'])]),
        ('KEY_G', '0x0a', [('g', []), ('G', ['KEY_LEFTSHIFT'])]),
        ('KEY_H', '0x0b', [('h', []), ('H', ['KEY_LEFTSHIFT'])]),
        ('KEY_I', '0x0c', [('i', []), ('I', ['KEY_LEFTSHIFT'])]),
        ('KEY_J', '0x0d', [('j', []), ('J', ['KEY_LEFTSHIFT'])]),
        ('KEY_K', '0x0e', [('k', []), ('K', ['KEY_LEFTSHIFT'])]),
        ('KEY_L', '0x0f', [('l', []), ('L', ['KEY_LEFTSHIFT'])]),
        ('KEY_M', '0x10', [('m', []), ('M', ['KEY_LEFTSHIFT'])]),
        ('KEY_N', '0x11', [('n', []), ('N', ['KEY_LEFTSHIFT'])]),
        ('KEY_O', '0x12', [('o', []), ('O', ['KEY_LEFTSHIFT'])]),
        ('KEY_P', '0x13', [('p', []), ('P', ['KEY_LEFTSHIFT'])]),
        ('KEY_Q', '0x14', [('q', []), ('Q', ['KEY_LEFTSHIFT'])]),
        ('KEY_R', '0x15', [('r', []), ('R', ['KEY_LEFTSHIFT'])]),
        ('KEY_S', '0x16', [('s', []), ('S', ['KEY_LEFTSHIFT'])]),
        ('KEY_T', '0x17', [('t', []), ('T', ['KEY_LEFTSHIFT'])]),
        ('KEY_U', '0x18', [('u', []), ('U', ['KEY_LEFTSHIFT'])]),
        ('KEY_V', '0x19', [('v', []), ('V', ['KEY_LEFTSHIFT'])]),
        ('KEY_W', '0x1a', [('w', []), ('W', ['KEY_LEFTSHIFT'])]),
        ('KEY_X', '0x1b', [('x', []), ('X', ['KEY_LEFTSHIFT'])]),
        ('KEY_Y', '0x1c', [('y', []), ('Y', ['KEY_LEFTSHIFT'])]),
        ('KEY_Z', '0x1d', [('z', []), ('Z', ['KEY_LEFTSHIFT'])]),
        ('KEY_1', '0x1e', [('1', []), ('!', ['KEY_LEFTSHIFT'])]),
        ('KEY_2', '0x1f', [('2', []), ('@', ['KEY_LEFTSHIFT'])]),
        ('KEY_3', '0x20', [('3', []), ('#', ['KEY_LEFTSHIFT'])]),
        ('KEY_4', '0x21', [('4', []), ('$', ['KEY_LEFTSHIFT'])]),
        ('KEY_5', '0x22', [('5', []), ('%', ['KEY_LEFTSHIFT'])]),
        ('KEY_6', '0x23', [('6', []), ('^', ['KEY_LEFTSHIFT'])]),
        ('KEY_7', '0x24', [('7', []), ('&', ['KEY_LEFTSHIFT'])]),
        ('KEY_8', '0x25', [('8', []), ('*', ['KEY_LEFTSHIFT'])]),
        ('KEY_9', '0x26', [('9', []), ('(', ['KEY_LEFTSHIFT'])]),
        ('KEY_0', '0x27', [('0', []), (')', ['KEY_LEFTSHIFT'])]),
        ('KEY_ENTER', '0x28', [('', [])]),
        ('KEY_ESC', '0x29', [('', [])]),
        ('KEY_BACKSPACE', '0x2a', [('', [])]),
        ('KEY_TAB', '0x2b', [('', [])]),
        ('KEY_SPACE', '0x2c', [(' ', [])]),
        ('KEY_MINUS', '0x2d', [('-', []), ('_', ['KEY_LEFTSHIFT'])]),
        ('KEY_EQUAL', '0x2e', [('=', []), ('+', ['KEY_LEFTSHIFT'])]),
        ('KEY_LEFTBRACE', '0x2f', [('[', []), ('{', ['KEY_LEFTSHIFT'])]),
        ('KEY_RIGHTBRACE', '0x30', [(']', []), ('}', ['KEY_LEFTSHIFT'])]),
        ('KEY_BACKSLASH', '0x31', [('\\', []), ('|', ['KEY_LEFTSHIFT'])]),
        ('KEY_SEMICOLON', '0x33', [(';', []), (':', ['KEY_LEFTSHIFT'])]),
        ('KEY_APOSTROPHE', '0x34', [('\'', []), ('"', ['KEY_LEFTSHIFT'])]),
        ('KEY_GRAVE', '0x35', [('`', []), ('~', ['KEY_LEFTSHIFT'])]),
        ('KEY_COMMA', '0x36', [(',', []), ('<', ['KEY_LEFTSHIFT'])]),
        ('KEY_DOT', '0x37', [('.', []), ('>', ['KEY_LEFTSHIFT'])]),
        ('KEY_SLASH', '0x38', [('/', []), ('?', ['KEY_LEFTSHIFT'])]),
        ('KEY_CAPSLOCK', '0x39', []),
        ('KEY_F1', '0x3a', [('', [])]),
        ('KEY_F2', '0x3b', [('', [])]),
        ('KEY_F3', '0x3c', [('', [])]),
        ('KEY_F4', '0x3d', [('', [])]),
        ('KEY_F5', '0x3e', [('', [])]),
        ('KEY_F6', '0x3f', [('', [])]),
        ('KEY_F7', '0x40', [('', [])]),
        ('KEY_F8', '0x41', [('', [])]),
        ('KEY_F9', '0x42', [('', [])]),
        ('KEY_F10', '0x43', [('', [])]),
        ('KEY_F11', '0x44', [('', [])]),
        ('KEY_F12', '0x45', [('', [])]),
        ('KEY_DELETE', '0x4c', [('', [])]),
        ('CTRL_ALT_DEL', '0x4c', [('', ['CTRL', 'ALT'])]),
        ('CTRL_C', '0x06', [('', ['CTRL'])]),
    ]

# code above was based on code from https://github.com/at-ohms/VMKey/blob/master/VMKey.py
# see also:
#   http://key-value.blogspot.com/2017/11/vmware-keystroke-based-automation.html
#   https://github.com/alanjcastonguay/send-keys-to-vm/blob/master/send_keys_to_vm.py
#
