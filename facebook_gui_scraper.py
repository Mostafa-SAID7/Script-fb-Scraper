import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from openpyxl import Workbook
import os
import pickle
import time
import threading

# === Setup ===
window = tk.Tk()
window.title("📘 Facebook Developer Scraper")
window.geometry("700x600")
window.resizable(False, False)

# === Dark Theme ===
DARK_BG = "#1e1e1e"
DARK_FG = "#f5f5f5"
ENTRY_BG = "#2b2b2b"
window.configure(bg=DARK_BG)

style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6, background="#3c3f41", foreground=DARK_FG)
style.configure("TLabel", font=("Segoe UI", 10), background=DARK_BG, foreground=DARK_FG)
style.configure("TProgressbar", background="#5c9ded")

def make_section(label_text):
    ttk.Label(window, text=label_text).pack(anchor='w', padx=10)

# === Input Fields ===
make_section("📎 Facebook Group URLs (one per line):")
entry_urls = tk.Text(window, height=6, width=85, font=("Consolas", 10), bg=ENTRY_BG, fg=DARK_FG, insertbackground=DARK_FG)
entry_urls.pack(padx=10)

make_section("🔑 Keywords (comma-separated):")
entry_keywords = tk.Entry(window, bg=ENTRY_BG, fg=DARK_FG, insertbackground=DARK_FG)
entry_keywords.insert(0, "C#, Angular, ASP.NET")
entry_keywords.pack(padx=10, fill='x')

make_section("🔁 Scroll count (for loading posts):")
entry_scrolls = tk.Entry(window, bg=ENTRY_BG, fg=DARK_FG, insertbackground=DARK_FG)
entry_scrolls.insert(0, "5")
entry_scrolls.pack(padx=10, fill='x')

make_section("📊 Minimum number of likes per post:")
entry_min_likes = tk.Entry(window, bg=ENTRY_BG, fg=DARK_FG, insertbackground=DARK_FG)
entry_min_likes.insert(0, "5")
entry_min_likes.pack(padx=10, fill='x')

# === Progress ===
progress_label = ttk.Label(window, text="Collected 0 profiles", foreground="lightgreen")
progress_label.pack(pady=5)

progress_bar = ttk.Progressbar(window, length=400, mode='indeterminate')
progress_bar.pack(pady=5)

log_box = tk.Text(window, height=10, width=85, font=("Consolas", 9), bg=ENTRY_BG, fg=DARK_FG, insertbackground=DARK_FG)
log_box.pack(padx=10, pady=5)

def log(msg):
    log_box.insert(tk.END, f"{msg}\n")
    log_box.see(tk.END)

# === Scraper ===
def run_scraper():
    try:
        keywords = [k.strip() for k in entry_keywords.get().split(",") if k.strip()]
        urls = entry_urls.get("1.0", tk.END).strip().splitlines()
        scroll_count = int(entry_scrolls.get())
        min_likes = int(entry_min_likes.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")
        return

    log("🚀 Starting the scraper...")

    collected = set()
    total_count = 0
    start_time = time.time()

    chromedriver_path = os.path.join(os.getcwd(), "chromedriver.exe")
    driver = webdriver.Chrome(service=Service(chromedriver_path))
    driver.get("https://www.facebook.com/")
    time.sleep(3)

    cookie_file = "facebook_cookies.pkl"

    if os.path.exists(cookie_file):
        log("🔐 Loading saved session cookies...")
        with open(cookie_file, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                try:
                    driver.add_cookie(cookie)
                except:
                    continue
        driver.get("https://www.facebook.com/")
        time.sleep(3)
    else:
        messagebox.showinfo("Login Required", "Please log in to Facebook manually in the opened browser.")
        input("📌 After logging in, return here and press Enter...")
        with open(cookie_file, "wb") as f:
            pickle.dump(driver.get_cookies(), f)
        log("✅ Cookies saved for future sessions.")

    wb = Workbook()
    ws = wb.active
    ws.append(["Profile Link", "Keyword", "Group URL", "Type"])
    progress_bar.start()

    for group_url in urls:
        log(f"🔍 Processing group: {group_url}")
        try:
            driver.get(group_url)
            time.sleep(5)

            for _ in range(scroll_count):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

            posts = driver.find_elements(By.XPATH, '//div[contains(@data-ad-preview, "message")]')
            for post in posts:
                try:
                    text = post.text
                    try:
                        likes_el = post.find_element(By.XPATH, './/span[contains(text(), "Like") or contains(text(), "likes")]')
                        likes = int(''.join(filter(str.isdigit, likes_el.text)))
                    except:
                        likes = 0

                    if likes < min_likes:
                        continue

                    for keyword in keywords:
                        if keyword.lower() in text.lower():
                            try:
                                profile_link = post.find_element(By.XPATH, './/a[contains(@href, "facebook.com")]').get_attribute("href").split("?")[0]
                                if profile_link not in collected:
                                    collected.add(profile_link)
                                    ws.append([profile_link, keyword, group_url, "Post"])
                                    total_count += 1
                                    progress_label.config(text=f"Collected: {total_count} profiles")
                            except:
                                continue
                except:
                    continue

            comments = driver.find_elements(By.XPATH, '//ul//a[contains(@href, "facebook.com") and not(contains(@href, "groups"))]')
            for comment in comments:
                try:
                    href = comment.get_attribute("href").split("?")[0]
                    if ("facebook.com/profile.php" in href or "/people/" in href) and href not in collected:
                        collected.add(href)
                        ws.append([href, "N/A", group_url, "Comment"])
                        total_count += 1
                        progress_label.config(text=f"Collected: {total_count} profiles")
                except:
                    continue
        except Exception as e:
            log(f"❌ Error in group {group_url}: {e}")

    filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if filename:
        wb.save(filename)
        messagebox.showinfo("Saved", f"{total_count} profiles saved to:\n{filename}")
        log(f"💾 Saved to: {filename}")

    driver.quit()
    progress_bar.stop()
    elapsed = round(time.time() - start_time, 2)
    log(f"🎉 Scraping completed in {elapsed} seconds.")
    progress_label.config(text="✅ Scraping Complete!")

# === Run in Thread ===
def start_thread():
    threading.Thread(target=run_scraper).start()

ttk.Button(window, text="Start Scraping ✅", command=start_thread).pack(pady=10)
window.mainloop()
