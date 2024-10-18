from evdev import InputDevice, categorize, ecodes, list_devices
import mido

# ( ͡° ͜ʖ ͡°) Open a MIDI output port
midi_out = mido.open_output('MazboardPrototype', virtual=True)

vendor_id = 0x258a
product_id = 0x0026

# Debug: (✧ω✧) List all available input devices
print("Available input devices:")  # (¬‿¬ )
for device in list_devices():
    print(device)  # (ʘ‿ʘ)

keyboard_device = None
devices = [InputDevice(path) for path in list_devices()]

for device in devices:
    if device.info.vendor == vendor_id and device.info.product == product_id:
        keyboard_device = device
        print(f"Found keyboard device: {device.name} at {device.path}")  # (╯°□°)╯
        break

if keyboard_device is None:
    print("Keyboard device not found! Please check the vendor and product IDs. :(")  # ಠ_ಠ
    exit(1)

# (╯°□°）╯ Define key-to-MIDI mapping
key_to_midi = {
    'KEY_A': 60,  # A -> MIDI note 60 (C4) (ง •̀_•́)ง
    'KEY_B': 62,  # B -> MIDI note 62 (D4) (ง ͡ʘ ͜ʖ ͡ʘ)ง
    'KEY_C': 64,  # C -> MIDI note 64 (E4) (ง •̀_•́)ง
    'KEY_D': 65,  # D -> MIDI note 65 (F4) (ง •̀_•́)ง
    'KEY_E': 67,  # E -> MIDI note 67 (G4) ヽ(ヅ)ノ
    'KEY_SPACE': 69,  # Space -> MIDI note 69 (A4) ✧･ﾟ: *✧･ﾟ:*
}

print("Listening to keyboard for MIDI events... ( ◕‿◕)")  # (^_^)

# (•̀ᴗ•́)و Mode variable
mode = "typewriter"  # ( •̀ω•́ ) Initial mode set to "typewriter mode"

# (¬‿¬) To track pressed keys in MIDI mode
pressed_keys = set()

def toggle_mode():
    """(⊙_⊙) Toggle between MIDI mode and Typewriter mode"""
    global mode
    if mode == "midi":
        release_all_midi_notes()  # (ง ͠° ͟ل͜ ͡°)ง Ensure all currently pressed keys are released before switching
        mode = "typewriter"
        enable_typing()  # ᕦ(ò_óˇ)ᕤ Enable typing in typewriter mode
    else:
        mode = "midi"
        disable_typing()  # ╭( ･ㅂ･)و Disable typing in MIDI mode
    print(f"Switched to mode: {mode}")  # ヾ(⌐■_■)ノ♪

def disable_typing():
    """(｡•̀ᴗ-)✧ Disable typing by using evdev's grab functionality"""
    try:
        keyboard_device.grab()  # (ᕗ ͡° ͜ʖ ͡°)ᕗ Prevent key events from being processed by the OS
        print("MIDI mode: typing disabled. (ノಠ益ಠ)ノ")
    except OSError as e:
        print(f"Error disabling typing: {e}")  # ヽ(ヅ)ノ

def enable_typing():
    """(ง ° ͜ʖ °) Enable typing by releasing the grab"""
    try:
        keyboard_device.ungrab()  # (ง •̀_•́)ง Allow key events to be processed by the OS
        print("Typewriter mode: typing enabled. (•̀ᴗ•́)و")
    except OSError as e:
        print(f"Error enabling typing: {e}")  # (✧ω✧)

def release_all_midi_notes():
    """Release all currently pressed MIDI notes ヽ(｀Д´)ﾉ"""
    for key in pressed_keys:
        midi_note = key_to_midi.get(key)
        if midi_note is not None:
            midi_out.send(mido.Message('note_off', note=midi_note))
            toggle_led(key, False)  # (ง •̀_•́)ง Turn off LED when key is released
            print(f"Released MIDI note for key: {key} ( ͡° ͜ʖ ͡°)")
    pressed_keys.clear()  # ( ͡ᵔ ͜ʖ ͡ᵔ) Clear the set of pressed keys

def toggle_led(key, state):
    """(⊙_⊙) Toggle LED based on the state and key pressed"""
    led_mapping = {
        'KEY_A': ecodes.LED_NUML,  # Num Lock LED for KEY_A (•̀ᴗ•́)و
        'KEY_B': ecodes.LED_CAPSL,  # Caps Lock LED for KEY_B (ง ͠° ͟ل͜ ͡°)ง
        'KEY_C': ecodes.LED_SCROLLL,  # Scroll Lock LED for KEY_C ヽ(ヅ)ノ
        # Add more mappings as needed ✧･ﾟ: *✧･ﾟ:*
    }
    
    if key in led_mapping:
        if state:
            # (ง •̀_•́)ง Turn on the LED for the specific key
            keyboard_device.write(ecodes.EV_LED, led_mapping[key], 1)  # (ノಠ益ಠ)ノ 1 to turn on
            print(f"LED on for key: {key} (¬‿¬ )")
        else:
            # (ง ͠° ͟ل͜ ͡°) Turn off the LED for the specific key
            keyboard_device.write(ecodes.EV_LED, led_mapping[key], 0)  # (ง •̀_•́)ง 0 to turn off
            print(f"LED off for key: {key} ヽ(ヅ)ノ")

# (｡•̀ᴗ-)✧ Use evdev to listen for key events
try:
    for event in keyboard_device.read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)

            # (ง ͡ʘ ͜ʖ ͡ʘ)ง Check for key press (event.value == 1)
            if event.value == 1:  # (ง ° ͜ʖ °) Key press (ignore key repeats)
                if mode == "midi":
                    # (ง •̀_•́)ง Send MIDI notes only in MIDI mode
                    midi_note = key_to_midi.get(key_event.keycode)
                    if midi_note:
                        pressed_keys.add(key_event.keycode)  # Track pressed key (ง ͠° ͟ل͜ ͡°)ง
                        midi_out.send(mido.Message('note_on', note=midi_note))
                        toggle_led(key_event.keycode, True)  # (╯°□°）╯ Turn on LED when key is pressed
                        print(f"Key pressed: {key_event.keycode}, MIDI note: {midi_note} (¬‿¬ )")

            elif event.value == 0:  # Key release ヽ(｀Д´)ﾉ
                # (ง •̀_•́)ง Toggle mode on Tab key release
                if key_event.keycode == 'KEY_TAB':
                    toggle_mode()
                    continue  # Skip further processing for the Tab key

                if mode == "midi":
                    # (ง ° ͜ʖ °) Stop sending MIDI notes on key release
                    midi_note = key_to_midi.get(key_event.keycode)
                    if midi_note:
                        pressed_keys.discard(key_event.keycode)  # Remove released key
                        midi_out.send(mido.Message('note_off', note=midi_note))
                        toggle_led(key_event.keycode, False)  # (ง •̀_•́)ง Turn off LED when key is released
                        print(f"Key released: {key_event.keycode}, MIDI note: {midi_note} ヽ(ヅ)ノ")

except KeyboardInterrupt:
    print("Exiting... (╯︵╰,)")
