import json
import time


def search_duckduckgo(query, max_results=6):
    results = []
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            raw = ddgs.text(query, max_results=max_results)
            if raw:
                for r in raw:
                    title = r.get("title", "بدون عنوان")
                    link = r.get("href", "")
                    snippet = r.get("body", "")

                    blocked_words = [
                        "ألغاز",
                        "مسابقات",
                        "ثقافية منوعة",
                        "ذكاء",
                        "ويكي السعودية",
                        "مصر",
                        "ثانوية عامة مصر"
                    ]
                    combined_text = f"{title} {snippet} {link}".lower()
                    if any(word in combined_text for word in blocked_words):
                        continue

                    results.append({
                        "title": title,
                        "link": link,
                        "snippet": snippet
                    })
    except Exception as e:
        print(f"تنبيه أثناء البحث ({query}): {e}")
    return results


def build_queries_for_subject(subject):
    if subject == "اللغة الإنجليزية":
        return [
            ("الفصل الأول واليونت الأول وحلولها", "اسئلة وحلول يونت 1 سادس علمي انكليزي العراق"),
            ("قواعد وتمارين وحلول", "قواعد وتمارين وحلول سادس علمي انكليزي العراق"),
            ("أسئلة وزارية مع الحل", "اسئلة وزارية انكليزي سادس علمي مع الحل العراق"),
        ]
    elif subject == "الإسلامية":
        return [
            ("الفصل الأول وأحكامه وحلوله", "اسئلة وحلول الفصل الاول اسلامية سادس علمي العراق"),
            ("أحكام التلاوة والمواضيع وحلولها", "احكام التلاوة وحلول اسئلة اسلامية سادس علمي العراق"),
            ("أسئلة وزارية مع الحل", "اسئلة وزارية اسلامية سادس علمي مع الحل العراق"),
        ]
    elif subject == "اللغة العربية":
        return [
            ("الفصل الأول وقواعده وحلوله", "اسئلة وحلول الفصل الاول قواعد عربي سادس علمي العراق"),
            ("الأدب والقواعد وحلول التمارين", "حل تمارين قواعد وادب سادس علمي العراق"),
            ("أسئلة وزارية مع الحل", "اسئلة وزارية لغة عربية سادس علمي مع الحل العراق"),
        ]
    else:
        return [
            ("الفصل الأول والأسئلة مع الحل", f"اسئلة وحلول الفصل الاول {subject} سادس علمي العراق"),
            ("القوانين والمسائل وحلولها", f"قوانين ومسائل وحلول {subject} سادس علمي العراق"),
            ("أسئلة وزارية مع الحل", f"اسئلة وزارية {subject} سادس علمي مع الحل العراق"),
        ]


def main():
    subjects = [
        "الرياضيات",
        "الفيزياء",
        "الكيمياء",
        "الأحياء",
        "اللغة الإنجليزية",
        "اللغة العربية",
        "الإسلامية",
    ]

    database = {}

    for subject in subjects:
        print(f"=== جاري جمع مواد وأسئلة وحلول: {subject} ===")
        subject_items = []
        seen_links = set()

        queries = build_queries_for_subject(subject)
        for category_label, query in queries:
            print(f"  - بحث ({category_label}): {query}")
            found = search_duckduckgo(query, max_results=5)

            for item in found:
                link = item.get("link", "")
                if link and link in seen_links:
                    continue
                if link:
                    seen_links.add(link)

                enriched_snippet = f"[{category_label}] {item.get('snippet', '')}".strip()
                subject_items.append({
                    "category": category_label,
                    "title": item.get("title", "بدون عنوان"),
                    "link": link,
                    "snippet": enriched_snippet,
                })

            time.sleep(1.5)

        database[subject] = subject_items
        time.sleep(2)

    with open("questions_data.json", "w", encoding="utf-8") as f:
        json.dump(database, f, ensure_ascii=False, indent=4)

    print("تم تحديث ملف questions_data.json بجميع مواد السادس العلمي بنجاح.")


if __name__ == "__main__":
    main()
