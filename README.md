# TextGrabber

A powerful screen capture utility that extracts text from non-copyable sources using OCR technology.

![TextGrabber Logo](assets/logo.png) <!-- Optional: Add your logo -->

## 🚀 Features

- **Quick Screen Capture**: Capture any portion of your screen with a simple hotkey (default: Ctrl+Shift+S)
- **Smart Text Extraction**: Advanced OCR processing using Tesseract
- **System Tray Integration**: Convenient access through system tray icon
  - Left-click to capture
  - Right-click for menu options
- **Intelligent Text Processing**:
  - Preserves file paths and URLs
  - Maintains special characters
  - Smart word spacing and formatting

## 📋 Requirements

- Python 3.12+
- Windows OS
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed (default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/TextGrabber.git
cd TextGrabber
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR if not already installed:
   - Download from [Tesseract Installer](https://github.com/UB-Mannheim/tesseract/wiki)
   - Install to default location (`C:\Program Files\Tesseract-OCR\`)

## 💻 Usage

1. Run the application:
```bash
python text_grabber.py
```

2. The app will minimize to system tray
3. Use the default hotkey (Ctrl+Shift+S) or left-click the tray icon to capture
4. Select the area containing text
5. Extracted text will be automatically copied to clipboard

## ⚙️ Configuration

Settings are stored in: `%APPDATA%/TextGrabber/settings.json`

Configurable options include:
- Hotkey combinations
- Tesseract OCR path
- Text processing preferences

## 🛠️ Dependencies

- `pytesseract`: OCR engine interface
- `Pillow`: Image processing
- `tkinter`: GUI components
- `keyboard`: Hotkey management
- `pystray`: System tray integration
- `pyperclip`: Clipboard operations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for the OCR engine
- All contributors and users of TextGrabber
