import pymongo

print("hello")
client = pymongo.MongoClient("localhost", 27017)
# db = client.test
# print(db.test_collection)
# import datetime
# post = {
#     "author": "Mike",
#     "text": "My first blog post!",
#     "tags": ["mongodb", "python", "pymongo"],
#     "date": datetime.datetime.now(tz=datetime.timezone.utc),
# }
# posts = db.posts
# post_id = posts.insert_one(post).inserted_id
# print(post_id)
from pprint import pprint, pformat

# pprint.pprint(posts.find_one())
# pprint.pprint(posts.find_one({"author": "Mike"}))
lib_db = client.library
books = lib_db.books
fl = 1
while fl != 0:
    fl = int(input("enter action: "))
    match fl:
        case 1:
            print("adding")
            title = input("enter title: ")
            author = input("enter author: ")
            year = int(input("enter year of publishing: "))
            mark = input("enter your mark if you want: ")
            # print(mark)
            # print(type(mark))
            if mark.isdigit():
                book_data = {
                    "title": title,
                    "author": author,
                    "year": year,
                    "ratings": [int(mark)],
                }
            else:
                book_data = {
                    "title": title,
                    "author": author,
                    "year": year,
                    "ratings": [],
                }
            res = books.insert_one(book_data)
            if res.acknowledged:
                print("the book was added")
            else:
                print("error while adding")
        case 2:
            title = input("removing book, enter title: ")
            print("deleted:\n", pformat(books.find_one_and_delete({"title": title})))
        case 3:
            print("finding by author")
            author = input("enter author: ")
            for book in books.find({"author": author}):
                pprint(book)
        case 4:
            print("update book year")
            title = input("enter the book to edit info: ")
            newyear = int(input("enter the year: "))
            print(
                "replaced:\n",
                pformat(
                    books.update_one({"title": title}, {"$set": {"year": newyear}})
                ),
            )
        case 5:
            print("showing all books...")
            for book in books.find():
                pprint(book)
        case 6:
            print("add mark")
            title = input("enter the book to edit info: ")
            mark = int(input("enter your mark: "))
            print(
                "added:\n",
                pformat(
                    books.update_one({"title": title}, {"$push": {"ratings": mark}})
                ),
            )
        case 7:
            print("view mark of: ")
            book = input("enter the book to view avg mark: ")
            print(
                list(
                    books.aggregate(
                        [
                            {"$match": {"title": book}},
                            {"$unwind": "$ratings"},
                            {
                                "$group": {
                                    "_id": "$_id",
                                    "avgValue": {"$avg": "$ratings"},
                                }
                            },
                        ]
                    )
                )[0]["avgValue"]
            )
