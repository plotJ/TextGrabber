import pytesseract
from PIL import Image, ImageGrab
import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip
import sys
import os
import re
import json
import keyboard
import pystray
from PIL import Image as PilImage
import threading
import winreg as reg

# Set Tesseract path - update this to your Tesseract installation path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class TextGrabber:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Text Grabber")
        self.root.withdraw()  # Hide main window by default
        
        # Load or create settings
        self.settings_file = os.path.join(os.getenv('APPDATA'), 'TextGrabber', 'settings.json')
        self.load_settings()
        
        # Create system tray icon
        self.setup_tray()
        
        # Register hotkey
        self.register_hotkey()
        
        # Create settings window
        self.settings_window = None
        
    def load_settings(self):
        default_settings = {
            'hotkey': 'ctrl+shift+s'
        }
        
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    self.settings = json.load(f)
            else:
                self.settings = default_settings
                with open(self.settings_file, 'w') as f:
                    json.dump(self.settings, f)
        except Exception:
            self.settings = default_settings

    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save settings: {str(e)}")

    def setup_tray(self):
        # Create system tray icon
        image = PilImage.new('RGB', (64, 64), color='white')
        menu = (
            pystray.MenuItem("Grab Text", self.capture_and_extract_text),
            pystray.MenuItem("Settings", self.show_settings),
            pystray.MenuItem("Exit", self.quit_app)
        )
        
        def on_click(icon, item):
            if item is None:  # Left click
                self.capture_and_extract_text()
            else:  # Right click menu item
                item()
        
        self.tray_icon = pystray.Icon("TextGrabber", image, "Text Grabber", menu)
        self.tray_icon.on_click = on_click
        
        # Start system tray icon in a separate thread
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def register_hotkey(self):
        try:
            # Unregister previous hotkey if exists
            keyboard.unhook_all()
            # Register new hotkey
            keyboard.add_hotkey(self.settings['hotkey'], self.capture_and_extract_text)
        except Exception as e:
            messagebox.showerror("Error", f"Could not register hotkey: {str(e)}")

    def show_settings(self):
        if self.settings_window is not None:
            self.settings_window.lift()
            return
            
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("300x150")
        self.settings_window.protocol("WM_DELETE_WINDOW", lambda: self.settings_window.withdraw())
        
        # Hotkey frame
        frame = ttk.Frame(self.settings_window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="Hotkey:").grid(row=0, column=0, sticky=tk.W)
        hotkey_var = tk.StringVar(value=self.settings['hotkey'])
        hotkey_entry = ttk.Entry(frame, textvariable=hotkey_var)
        hotkey_entry.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        def save_settings():
            new_hotkey = hotkey_var.get()
            try:
                # Test if hotkey is valid
                keyboard.parse_hotkey(new_hotkey)
                self.settings['hotkey'] = new_hotkey
                self.save_settings()
                self.register_hotkey()
                self.settings_window.withdraw()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid hotkey: {str(e)}")
        
        ttk.Button(frame, text="Save", command=save_settings).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Center the window
        self.settings_window.update_idletasks()
        width = self.settings_window.winfo_width()
        height = self.settings_window.winfo_height()
        x = (self.settings_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.settings_window.winfo_screenheight() // 2) - (height // 2)
        self.settings_window.geometry(f'{width}x{height}+{x}+{y}')

    def quit_app(self):
        self.tray_icon.stop()
        self.root.quit()

    def clean_text(self, text):
        # Remove single characters that are likely noise (except common single-letter words)
        valid_single_chars = {'a', 'i', 'A', 'I'}
        
        # First preserve path separators and special characters
        replacements = {
            '\\': ' <BACKSLASH> ',
            '/': ' <FORWARDSLASH> ',
            '(': ' <LEFTPAREN> ',
            ')': ' <RIGHTPAREN> ',
            ':': ' <COLON> ',
        }
        
        # Replace special characters with placeholders
        for char, placeholder in replacements.items():
            text = text.replace(char, placeholder)
        
        # Replace multiple spaces and newlines with single space
        text = ' '.join(text.split())
        
        # Split into words and filter
        words = text.split()
        cleaned_words = []
        
        for word in words:
            # Skip placeholder words
            if word.startswith('<') and word.endswith('>'):
                continue
                
            # Keep word if:
            # 1. It's longer than 1 character, or
            # 2. It's a valid single character
            # 3. It contains at least one alphanumeric character
            if (len(word) > 1 or word in valid_single_chars) and any(c.isalnum() for c in word):
                cleaned_words.append(word)
        
        # Join words with proper spacing
        text = ' '.join(cleaned_words)
        
        # Restore special characters
        for char, placeholder in replacements.items():
            text = text.replace(placeholder, char)
        
        return text

    def capture_and_extract_text(self):
        try:
            # Create a fullscreen transparent window
            self.overlay = tk.Toplevel(self.root)
            self.overlay.attributes('-alpha', 0.3)
            self.overlay.attributes('-fullscreen', True)
            self.overlay.attributes('-topmost', True)
            
            # Bind mouse events
            self.overlay.bind('<Button-1>', self.on_mouse_down)
            self.overlay.bind('<B1-Motion>', self.on_mouse_drag)
            self.overlay.bind('<ButtonRelease-1>', self.on_mouse_up)
            self.overlay.bind('<Escape>', lambda e: self.overlay.destroy())
            
            # Wait until selection is made
            self.overlay.wait_window()
            
            if hasattr(self, 'selection_made') and self.selection_made and hasattr(self, 'bbox'):
                # Capture the selected region
                screenshot = ImageGrab.grab(bbox=self.bbox)
                
                # Use Tesseract to do OCR with confidence scores
                data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
                
                # Extract text with confidence above threshold
                threshold = 60  # Minimum confidence score
                extracted_text = []
                
                for i in range(len(data['text'])):
                    try:
                        confidence = float(data['conf'][i])
                        if confidence > threshold:
                            text = data['text'][i].strip()
                            if text:
                                extracted_text.append(text)
                    except (ValueError, TypeError):
                        continue
                
                # Join and clean the text
                final_text = self.clean_text(' '.join(extracted_text))
                
                # Copy to clipboard if text was found
                if final_text:
                    pyperclip.copy(final_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.selection_made = False

    def on_mouse_drag(self, event):
        if hasattr(self.overlay, 'canvas'):
            self.overlay.canvas.destroy()
        
        self.overlay.canvas = tk.Canvas(self.overlay)
        self.overlay.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, 
                                          outline='red', width=2)
        self.overlay.canvas.place(relwidth=1, relheight=1)

    def on_mouse_up(self, event):
        # Store the bounding box coordinates
        self.bbox = (min(self.start_x, event.x), 
                    min(self.start_y, event.y),
                    max(self.start_x, event.x), 
                    max(self.start_y, event.y))
        self.selection_made = True
        self.overlay.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = TextGrabber()
    app.run()
