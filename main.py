import os
import numpy as np


class Lib:
    num_books = None
    signup = None
    book_per_day = None
    books = None
    id = None
    days_running = None
    books_scanned = None

    def get_points_of_all_books(self):
        sum = 0
        for book in self.books:
            sum += scores[book]
        return sum

    def get_ratio(self):
        return (self.signup, (1/float(len(self.books))))

    def __cmp__(self, other):
        return cmp(self.get_ratio(), other.get_ratio())


def get_score(id):
    return scores[id]


num_books = None
num_libraries = None
days_total = None
scores = None
libs = []

file_names = [
    "a_example",
    "b_read_on",
    "c_incunabula",
    "d_tough_choices",
    "e_so_many_books",
    "f_libraries_of_the_world"
]

FILE_TO_RUN = 5
file_name = file_names[FILE_TO_RUN]

# INPUT
inputfile = os.path.join("io", file_name + ".txt")
f = open(inputfile,"r")
lines = f.readlines()

lib = None
lib_id = 0

for i, x in enumerate(lines):
    line = x.split(' ')
    if i == 0:
        num_books = int(line[0])
        num_libraries = int(line[1])
        days_total = int(line[2])
        continue

    if i == 1:
        scores = np.asarray(map(int, line))
        continue

    if lib is None:
        lib = Lib()
        lib.id = lib_id
        lib.num_books = int(line[0])
        lib.signup = int(line[1])
        lib.book_per_day = int(line[2])
    else:
        lib.books = np.asarray(map(int, line))
        libs.append(lib)
        lib_id += 1
        lib = None

# END INPUT


# REMOVE DUPLICATE BOOKS FROM ONGOING LIBS
# for i, lib in enumerate(libs):
#     uniques = lib.books
#     print(str(i) + " / " + str(len(libs)))
#     for j, lib_other in enumerate(libs):
#         if i > j:
#             uniques = [v for v in uniques if v not in lib_other.books]
#     lib.books = uniques


# SCHEDULE LIBRARIES
final_libs = []
libs.sort()

days_running = 0
for lib in libs:
    if not (days_running + lib.signup <= days_total):
        break

    days_running += lib.signup
    lib.days_running = days_running
    final_libs.append(lib)

books_read = []

# REMOVE DUPLICATED BOOKS AFTER SCHEDULING
for j, lib in enumerate(final_libs):
    lib.books = sorted(lib.books, key=get_score, reverse=True)
    books_to_scan = min((days_total - lib.days_running) * lib.book_per_day, len(lib.books))

    # print(str(j) + " / " + str(len(final_libs)))
    books_for_lib = []
    for i, book in enumerate(lib.books):
        if len(books_for_lib) >= books_to_scan:
            break

        if book not in books_read:
            books_read.append(book)
            books_for_lib.append(book)


# CALCULATE RUNNING DAYS AND MAXIMUM BOOKS PER LIB
for lib in final_libs:
    lib.books_scanned = min((days_total - lib.days_running) * lib.book_per_day, len(lib.books))
    lib.books = sorted(lib.books, key=get_score, reverse=True)
    lib.books = lib.books[:lib.books_scanned]


# OUTPUT
outputfile = os.path.join("io", file_name + "_output.txt")
o = open(outputfile,"w+")
o.write(str(len(final_libs)) + "\n")
for lib in final_libs:
    o.write(str(lib.id) + " " + str(lib.books_scanned) + "\n")
    o.write(" ".join(map(str, lib.books)) + "\n")

o.close()