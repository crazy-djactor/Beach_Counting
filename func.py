
import csv
import os


def append_csv(filename, data):
    """
        save the "data" to filename as csv format.
    """
    file_out = open(filename, 'a')
    writer = csv.writer(file_out)
    writer.writerows(data)
    file_out.close()


def save_csv(filename, data):
    """
        save the "data" to filename as csv format.
    """
    file_out = open(filename, 'w')
    writer = csv.writer(file_out)
    writer.writerows(data)
    file_out.close()


def load_csv(filename):
    """
        load the csv data and return it.
    """
    if os.path.isfile(filename):
        file_csv = open(filename, 'r')
        reader = csv.reader(file_csv)
        data_csv = []
        for row_data in reader:
            data_csv.append(row_data)

        file_csv.close()
        return data_csv
    else:
        return []


def load_text(filename):
    if os.path.isfile(filename):
        f = open(filename, 'r')
        data = f.read()
        f.close()
        return data
    else:
        return []


def save_text(filename, data):
    f = open(filename, 'w')
    f.write(data)
    f.close()


def check_rect_overlap(rect1, rect2):
    min_x1 = min(rect1[0], rect1[2])
    max_x1 = max(rect1[0], rect1[2])
    min_y1 = min(rect1[1], rect1[3])
    max_y1 = max(rect1[1], rect1[3])

    min_x2 = min(rect2[0], rect2[2])
    max_x2 = max(rect2[0], rect2[2])
    min_y2 = min(rect2[1], rect2[3])
    max_y2 = max(rect2[1], rect2[3])

    if max_x1 < min_x2 or max_x2 < min_x1 or max_y1 < min_y2 or max_y2 < min_y1:
        return False
    else:
        return True


def check_contain(rect_list, rect):
    f_same = True
    for j in range(len(rect_list)):
        prev_rect = rect_list[j]
        f_same = True
        for k in range(4):
            if abs(prev_rect[k] - rect[k]) > 10:
                f_same = False
                break

        if f_same:
            break

    return f_same


def rm_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)
