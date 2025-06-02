import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook
import time
import threading

# === GUI Setup ===
window = tk.Tk()
window.title("📘 Facebook Developer Scraper")
window.geometry("700x600")
window.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
style.configure("TLabel", font=("Segoe UI", 10), padding=4)

def make_section(label_text):
    ttk.Label(window, text=label_text, font=("Segoe UI", 10, "bold")).pack(anchor='w', padx=10)

make_section("📎 Facebook Group URLs (one per line):")
entry_urls = tk.Text(window, height=6, width=85, font=("Consolas", 10))
entry_urls.pack(padx=10)

make_section("🔑 Keywords to search for (comma-separated):")
entry_keywords = tk.Entry(window)
entry_keywords.insert(0, "C#, Angular, ASP.NET")
entry_keywords.pack(padx=10, fill='x')

make_section("🔁 Scroll count (to load more posts):")
entry_scrolls = tk.Entry(window)
entry_scrolls.insert(0, "5")
entry_scrolls.pack(padx=10, fill='x')

make_section("📊 Minimum likes to accept a post:")
entry_min_likes = tk.Entry(window)
entry_min_likes.insert(0, "5")
entry_min_likes.pack(padx=10, fill='x')

# Progress and status
progress_label = ttk.Label(window, text="Collected 0 profiles", foreground="green")
progress_label.pack(pady=5)

progress_bar = ttk.Progressbar(window, length=400, mode='indeterminate')
progress_bar.pack(pady=5)

log_box = tk.Text(window, height=10, width=85, font=("Consolas", 9), bg="#f8f8f8")
log_box.pack(padx=10, pady=5)

def log(msg):
    log_box.insert(tk.END, f"{msg}\n")
    log_box.see(tk.END)

# ==== Scraper Core ====
def run_scraper():
    try:
        keywords = [k.strip() for k in entry_keywords.get().split(",") if k.strip()]
        urls = entry_urls.get("1.0", tk.END).strip().splitlines()
        scroll_count = int(entry_scrolls.get())
        min_likes = int(entry_min_likes.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for scroll count and minimum likes.")
        return

    messagebox.showinfo("Login Required", "Chrome will open. Please log in to Facebook manually first.")
    log("🚀 Starting scraper...")

    start_time = time.time()
    collected = set()
    total_count = 0

    driver = webdriver.Chrome()
    driver.get("https://www.facebook.com/")
    time.sleep(3)
    input("📌 After logging in, return here and press Enter...")

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
                        likes_text = likes_el.text
                        likes = int(''.join(filter(str.isdigit, likes_text)))
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
        messagebox.showinfo("Saved", f"Successfully saved {total_count} profiles to:\n{filename}")
        log(f"💾 Data saved to: {filename}")

    driver.quit()
    progress_bar.stop()
    elapsed = round(time.time() - start_time, 2)
    log(f"🎉 Scraping complete in {elapsed} seconds.")
    progress_label.config(text="✅ Scraping Complete!")

# ==== Thread Launcher ====
def start_thread():
    threading.Thread(target=run_scraper).start()

ttk.Button(window, text="Start Scraping ✅", command=start_thread).pack(pady=10)
window.mainloop()
