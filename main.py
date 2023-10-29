import re
import csv


def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        rows = csv.reader(file, delimiter=',')
        contact_list = list(rows)
        return contact_list


def file_formatting(contact_list):
    pattern = re.compile(r"(\+7|8)\s*\(?(\d{3})\)?\s*\-*(\d{3})\s*\-*(\d{2})\s*\-*(\d{2})\s*\(?(доб.|)\s*(\d*|)\)*")

    for row in contact_list[1:]:
        if len(re.findall(r"\w+", row[0])) > 1:
            for i, x in enumerate(re.findall(r"\w+", row[0])):
                row[i] = x

        if len(re.findall(r"\w+", row[1])) > 1:
            for i, x in enumerate(re.findall(r"\w+", row[1])):
                row[i+1] = x

        if len(re.findall(r"\w+", row[2])) > 1:
            for i, x in enumerate(re.findall(r"\w+", row[2])):
                row[i+2] = x

        row[5] = pattern.sub(r"+7(\2)\3-\4-\5 \6\7", row[5]).strip()

    return contact_list


def duplicate_removal(contact_list):
    contact_dict = {}
    for row in contact_list[1:]:
        contact_dict.setdefault(' '.join(row[:2]), row[2:])
        if ' '.join(row[:2]) in contact_dict.keys():
            for idx, field in enumerate(row[2:]):
                if field != '':
                    contact_dict[' '.join(row[:2])][idx] = row[idx + 2]

    result = [contact_list[0]]
    idx = 1
    for key, value in contact_dict.items():
        result.append([key.split()[0], key.split()[1]])
        [result[idx].append(field) for field in value]
        idx += 1
    return result


def write_file(path, contact_list):
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(contact_list)


if __name__ == '__main__':
    contact_list = file_formatting(read_file("phonebook_raw.csv"))
    contact_list = duplicate_removal(contact_list)
    write_file("phonebook_raw(formatted).csv", contact_list)