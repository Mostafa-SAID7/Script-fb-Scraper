import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook
import time
import threading

# ==== إعداد الواجهة ====
window = tk.Tk()
window.title("📘 Facebook Developer Scraper")

tk.Label(window, text="📎 روابط مجموعات فيسبوك (كل سطر = مجموعة):").pack()
entry_urls = tk.Text(window, height=6, width=80)
entry_urls.pack()

tk.Label(window, text="🔁 عدد مرات التمرير للأسفل (كلما زاد زادت النتائج):").pack()
entry_scrolls = tk.Entry(window)
entry_scrolls.insert(0, "5")
entry_scrolls.pack()

tk.Label(window, text="📊 عدد الإعجابات الأدنى لقبول المنشور:").pack()
entry_min_likes = tk.Entry(window)
entry_min_likes.insert(0, "5")
entry_min_likes.pack()

progress_label = tk.Label(window, text="تم جمع 0 حساب")
progress_label.pack()
progress_bar = ttk.Progressbar(window, length=400, mode='indeterminate')
progress_bar.pack(pady=5)

# ==== الوظيفة الأساسية ====
def run_scraper():
    keywords = ["C#", "Angular", "ASP.NET"]
    urls = entry_urls.get("1.0", tk.END).strip().splitlines()
    scroll_count = int(entry_scrolls.get())
    min_likes = int(entry_min_likes.get())

    messagebox.showinfo("تنبيه", "سيفتح Chrome لتسجيل الدخول. يرجى تسجيل الدخول يدويًا أولاً.")

    driver = webdriver.Chrome()
    driver.get("https://www.facebook.com/")
    time.sleep(3)
    input("📌 بعد تسجيل الدخول، ارجع لهذه النافذة واضغط Enter في الكونسول...")

    wb = Workbook()
    ws = wb.active
    ws.append(["Profile Link", "Keyword", "Group URL", "Type"])
    collected = set()
    total_count = 0

    progress_bar.start()

    for group_url in urls:
        driver.get(group_url)
        time.sleep(5)
        for _ in range(scroll_count):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        posts = driver.find_elements(By.XPATH, '//div[contains(@data-ad-preview, "message")]')

        for post in posts:
            try:
                text = post.text
                # فلترة بالإعجابات
                try:
                    likes_el = post.find_element(By.XPATH, './/span[contains(text(), "أعجب") or contains(text(), "Like")]')
                    likes_text = likes_el.text
                    likes = int(''.join(filter(str.isdigit, likes_text)))
                except:
                    likes = 0

                if likes < min_likes:
                    continue

                for keyword in keywords:
                    if keyword.lower() in text.lower():
                        try:
                            profile_link = post.find_element(By.XPATH, './/a[contains(@href, "facebook.com")]').get_attribute("href")
                            profile_link = profile_link.split("?")[0]
                            if profile_link not in collected:
                                collected.add(profile_link)
                                ws.append([profile_link, keyword, group_url, "Post"])
                                total_count += 1
                                progress_label.config(text=f"✅ تم جمع: {total_count} حساب")
                        except:
                            continue
            except:
                continue

        # التعليقات
        comments = driver.find_elements(By.XPATH, '//ul//a[contains(@href, "facebook.com") and not(contains(@href, "groups"))]')
        for comment in comments:
            try:
                href = comment.get_attribute("href")
                if href and ("facebook.com/profile.php" in href or "/people/" in href):
                    href = href.split("?")[0]
                    if href not in collected:
                        collected.add(href)
                        ws.append([href, "N/A", group_url, "Comment"])
                        total_count += 1
                        progress_label.config(text=f"✅ تم جمع: {total_count} حساب")
            except:
                continue

    filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if filename:
        wb.save(filename)
        messagebox.showinfo("✅ تم", f"تم حفظ {total_count} حساب في الملف:\n{filename}")

    driver.quit()
    progress_bar.stop()
    progress_label.config(text="🎉 الاستخراج اكتمل!")

# ==== تشغيل في خيط مستقل ====
def start_thread():
    threading.Thread(target=run_scraper).start()

tk.Button(window, text="تشغيل السكربت ✅", command=start_thread, bg="green", fg="white").pack(pady=10)
window.mainloop()
