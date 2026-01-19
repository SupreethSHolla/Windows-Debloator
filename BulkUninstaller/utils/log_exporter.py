import csv


def export_log_txt(lines, path):
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def export_log_csv(lines, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Message"])
        for line in lines:
            if "] " in line:
                t, m = line.split("] ", 1)
                writer.writerow([t.strip("["), m])
            else:
                writer.writerow(["", line])
