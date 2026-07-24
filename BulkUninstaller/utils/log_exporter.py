import csv


def export_log_txt(lines, path):
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def export_log_csv(lines, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Category", "Message"])
        for line in lines:
            if "] " in line:
                timestamp, remainder = line.split("] ", 1)
                category = ""
                message = remainder
                if remainder.startswith("[") and "] " in remainder:
                    category, message = remainder.split("] ", 1)
                    category = category.strip("[")
                writer.writerow([timestamp.strip("["), category, message])
            else:
                writer.writerow(["", "", line])
