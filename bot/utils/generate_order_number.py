import datetime
import pickle


def generate_order_number():
    date = datetime.datetime.utcnow().strftime("%d-%m-%Y")
    try:
        with open("db.txt", 'rb') as f:
            db = pickle.load(f)
        with open("db.txt", 'wb') as f:
            if date not in db.keys():
                db[date] = 1
                pickle.dump(db, f)
            else:
                db[date] += 1
                pickle.dump(db, f)
            order_number = date + "-" + str(db[date])
    except FileNotFoundError as e:
        f = open("db.txt", "wb")
        db = {date: 1}
        pickle.dump(db, f)
        order_number = date + "-" + str(1)
        f.close()
    return order_number


if __name__ == '__main__':
    print(generate_order_number())
