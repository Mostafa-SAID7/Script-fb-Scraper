# 📘 Facebook Developer Scraper

A powerful GUI tool for scraping Facebook group posts and comments to extract developer-related profile links based on custom keywords. Built with Python, Selenium, and Tkinter, it features:

- 🌙 Dark mode interface  
- 🔐 Auto-login via cookies  
- 🧾 Export to Excel  
- 🧳 Embedded ChromeDriver  
- 🖼️ Custom icon support  
- 📦 One-click `.exe` build  

---

## 🚀 Features

- 🎨 Dark-themed modern GUI
- 🔍 Keyword filtering (e.g., `C#`, `Angular`, `ASP.NET`)
- 🔁 Adjustable scroll depth per group
- ❤️ Filter by minimum post likes
- 💬 Profile extraction from posts **and** comments
- 🔐 Persistent login using Facebook cookies
- 💾 Save results to Excel `.xlsx`
- 🖱️ Standalone `.exe` support with app icon

---

## 📥 Download

<a href="https://your-download-link.com/facebook_scraper_gui.exe" target="_blank">
  <img src="https://img.shields.io/badge/Download_Executable-.EXE-green?style=for-the-badge&logo=windows&logoColor=white" alt="Download .EXE" />
</a>

> ✅ Requires Chrome browser installed

---

## 🧰 Requirements

- Python 3.8+
- Google Chrome
- ChromeDriver (auto-bundled in `.exe`)
- Facebook account

---

## ⚙️ Setup Guide (Python Users)

### 1. Clone the Project

```bash

git clone https://github.com/yourusername/facebook-scraper.git
cd facebook-scraper

2. Install Dependencies

pip install -r requirements.txt

Or manually:

pip install selenium openpyxl
```
3. Download & Place ChromeDriver

Visit Chrome for Testing

Download the version matching your Chrome

Extract chromedriver.exe into the project folder

## ▶️ Running the App
```
python facebook_scraper_gui.py
```
First time:

Login to Facebook in the opened browser

Press Enter in the terminal after logging in

Your session is saved for next time (via cookies)

#### 🧱 Build .EXE (Optional)
1. Install PyInstaller
```
pip install pyinstaller

2. Run Build Command

pyinstaller --onefile --windowed --icon=icon.ico --add-data "chromedriver.exe;." facebook_scraper_gui.py
This generates dist/facebook_scraper_gui.exe
You can now run it like any regular Windows app.
```
#### 📤 Output
The app saves an Excel .xlsx file with these columns:

Profile Link	Keyword	Group URL	Type
URL	C#	Group URL	Post
URL	N/A	Group URL	Comment

## 📁 Folder Structure
```
facebook_scraper/
├── facebook_scraper_gui.py
├── chromedriver.exe
├── icon.ico
├── requirements.txt
├── README.md
📃 License
```
1. This project is intended for educational and ethical use only.
2. You must comply with Facebook's Terms of Service.

## 🙌 Credits
- UI: Tkinter
- Automation: Selenium WebDriver
- Excel Export: OpenPyXL
- Icon Design: favicon.io
- Badge: shields.io
