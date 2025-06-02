# 📘 Facebook Developer Scraper

A simple GUI-based tool using **Tkinter**, **Selenium**, and **OpenPyXL** that extracts Facebook profile links from posts and comments in public Facebook groups based on specific keywords and minimum likes. Designed especially for developers or recruiters searching for posts mentioning technologies like `C#`, `Angular`, or `ASP.NET`.

---

## 🧰 Features

- 🔍 Scrapes Facebook group posts for keywords (`C#`, `Angular`, `ASP.NET`)
- 📥 Extracts profile links from posts and comments
- ❤️ Filters posts based on minimum number of likes
- 📂 Saves results in an Excel `.xlsx` file
- 📊 GUI progress bar and status updates

---

## 📦 Requirements

Ensure you have the following Python packages installed:

```bash
pip install selenium openpyxl
```
You also need:

Google Chrome installed

ChromeDriver that matches your Chrome version (and is added to your system PATH)
## How to Use
Run the Script:
```
python facebook_scraper_gui.py
Input Details:
```
Paste one or more Facebook group URLs

Set the number of times to scroll down (more scrolls = more posts)

Set the minimum number of likes a post must have to be included

Login to Facebook:

A Chrome window will open. Log into your Facebook account manually.

After logging in, return to the terminal and press Enter.

Scraping Starts Automatically:

Progress will show in the GUI

After scraping, you'll be prompted to save the results to an Excel file

## 📁 Output
The saved .xlsx file contains:

Profile Link	Keyword	Group URL	Type
...	C#	...	Post
...	N/A	...	Comment

## ⚠️ Notes
This script does not bypass Facebook login or scraping protections. It's meant for educational and personal use only.

You must log in manually when the browser opens.

Ensure that the groups you're scraping are public or accessible after login.

Excessive scraping may violate Facebook's terms of service — use responsibly.

## 🧑‍💻 Customization
Keywords can be modified in the keywords list inside the script:
keywords = ["C#", "Angular", "ASP.NET"]
To support other languages or frameworks, just add more keywords.

## 📜 License
This project is licensed for personal/educational use only. Not intended for commercial use.

You can save this content to a file named `README.md` in your project directory.
