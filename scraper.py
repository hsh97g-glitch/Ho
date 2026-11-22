import json
import time


def search_duckduckgo(query, max_results=10):
    results = []
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            raw = ddgs.text(query, max_results=max_results)
            if raw:
                for r in raw:
                    results.append({
                        "title": r.get("title", "بدون عنوان"),
                        "link": r.get("href", ""),
                        "snippet": r.get("body", "")
                    })
    except Exception as e:
        print(f"تنبيه أثناء البحث ({query}): {e}")
    return results


def main():
    subjects = [
        "الفيزياء",
        "الكيمياء",
        "الرياضيات",
        "الاحياء",
        "اللغة العربية",
        "اللغة الانجليزية"
    ]

    database = {}
    for subject in subjects:
        query = f"اسئلة وزارية {subject} السادس الاعدادي pdf"
        print(f"جاري البحث عن: {subject}...")
        database[subject] = search_duckduckgo(query, max_results=10)
        time.sleep(2)

    with open("questions_data.json", "w", encoding="utf-8") as f:
        json.dump(database, f, ensure_ascii=False, indent=4)

    print("تم إنشاء ملف questions_data.json بنجاح.")


if __name__ == "__main__":
    main()
