import time
import user
from random import randint

_book_catalog = {}
_author_lst = []
_deleted = set()


def __add(author, title):
    global _book_catalog, _author_lst, _deleted
    if author not in _book_catalog:
        _author_lst.append(author)
        _book_catalog[author] = set()

    _book_catalog[author].add(title)
    user.addBook(author, title)
    try:
        _deleted.remove((author, title))
    except KeyError:
        pass


def readData(fname):
    global _book_catalog, _author_lst
    _book_catalog = {}
    _author_lst = []
    with open(fname, encoding='utf-8') as f_in:
        for line in f_in:
            book = line.strip().split('=')
            author, title = book[0], book[1]
            __add(author, title)


def generate_invalid(N):
    global _deleted
    for i in range(N):
        chars = randint(2, 20)
        l_name = ""
        for j in range(chars):
            ch = randint(0, 25)
            l_name += chr(ord('a') + ch)

        chars = randint(2, 20)
        f_name = ""
        for j in range(chars):
            ch = randint(0, 25)
            f_name += chr(ord('a') + ch)

        author = l_name + " " + f_name
        title = "_invalid"
        _deleted.add((author, title))


def checkFind():
    global _book_catalog, _author_lst

    size = len(_author_lst)
    while True:
        author_num = randint(0, size - 1)
        author = _author_lst[author_num]

        books = list(_book_catalog[author])
        books_num = len(books)
        if books_num == 0:
            continue

        book_num = randint(0, books_num - 1)
        title = books[book_num]

        t = time.time()
        user_find = user.find(author, title)
        t1 = time.time()
        dt = t1 - t
        dt *= 100000

        if user_find and dt < 800:
            return True
        return False


def checkFindDeleted():
    global _book_catalog, _author_lst, _deleted

    size = len(_deleted)
    if size == 0:
        return True

    num = randint(0, size - 1)
    (author, title) = list(_deleted)[num]

    t = time.time()
    user_find = user.find(author, title)
    t1 = time.time()
    dt = t1 - t
    dt *= 100000
    if user_find:
        print(user.ff(author))
        print(title, user_find)
    if not user_find and dt < 800:
        return True
    return False


def checkFindAuthor():
    global _book_catalog, _author_lst

    size = len(_author_lst)

    num = randint(0, size - 1)
    author = _author_lst[num]

    books_num = len(_book_catalog[author])

    t = time.time()
    user_find = user.findByAuthor(author)
    t1 = time.time()
    dt = t1 - t
    dt *= 100000
    if len(user_find) == books_num and dt < 800:
        return True
    return False


def _delete():
    global _book_catalog, _author_lst, _deleted
    size = len(_author_lst)
    while True:
        author_num = randint(0, size - 1)
        author = _author_lst[author_num]

        if len(_book_catalog[author]) == 0:
            continue

        books = list(_book_catalog[author])
        books_num = len(books)

        num = randint(0, books_num - 1)
        title = books[num]

        _book_catalog[author].remove(title)
        _deleted.add((author, title))

        t = time.time()
        user.delete(author, title)
        t1 = time.time()
        dt = t1 - t
        dt *= 100000

        if dt < 800:
            return True
        return False


def restoreDeleted():
    global _book_catalog, _deleted

    size = len(_deleted)

    num = randint(0, size - 1)
    pair = list(_deleted)[num]
    _deleted.remove(pair)
    __add(*pair)

    t = time.time()
    user_find = user.find(*pair)
    t1 = time.time()
    dt = t1 - t
    dt *= 100000

    if user_find and dt < 800:
        return True
    return False


def main():
    global _book_catalog, _author_lst, _deleted

    _book_catalog = {}
    _author_lst = []
    _deleted = set()

    user.init()

    readData("data/library.txt")
    generate_invalid(500)

    test_num = 100000
    error = 0

    for i in range(test_num):
        case = randint(0, 4)
        res = True
        if case == 0:
            res = _delete()
        elif case == 1:
            res = checkFind()
        elif case == 2:
            res = checkFindDeleted()
        elif case == 3:
            res = checkFindAuthor()
        elif case == 4:
            res = restoreDeleted()

        if not res:
            print((case,i))
            error += 1

    valid_score = (test_num - error) / test_num
    score = 100 * valid_score
    print("Score: %d%%" % score)
    user.pr()


if __name__ == "__main__":
    main()