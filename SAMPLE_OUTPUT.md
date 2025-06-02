# Sample Output

---

This is a sample snapshot of the data exported by the **Facebook Developer Scraper** to an Excel file (`.xlsx`).

Each row represents a unique Facebook profile found either in posts or comments, filtered by your configured keywords and minimum likes.

---

## Excel Columns

| Profile Link                                      | Keyword    | Group URL                            | Type    |
| ------------------------------------------------ | ---------- | ---------------------------------- | ------- |
| https://www.facebook.com/john.doe                 | C#         | https://www.facebook.com/groups/123 | Post    |
| https://www.facebook.com/jane.smith               | Angular    | https://www.facebook.com/groups/123 | Post    |
| https://www.facebook.com/profile.php?id=10001122  | N/A        | https://www.facebook.com/groups/123 | Comment |
| https://www.facebook.com/dev.user                  | ASP.NET    | https://www.facebook.com/groups/456 | Post    |

---

## Explanation of Columns

- **Profile Link**: The direct URL to the Facebook user profile scraped from posts or comments.  
- **Keyword**: The keyword from your list (e.g., C#, Angular) matched in the post content. Comments have "N/A" since no keyword filtering applies.  
- **Group URL**: The Facebook group URL where the post or comment was found.  
- **Type**: Indicates if the profile was found in a "Post" or a "Comment".

---

## Notes

- Profiles are filtered to avoid duplicates.  
- Only posts with likes greater than or equal to the configured minimum are included.  
- The scraper requires manual Facebook login in Chrome before running.  
- Output file format is Excel `.xlsx`.

---

*This sample data is for demonstration purposes only and does not contain real user information.*
