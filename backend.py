import sqlite3


def init_db():
    con = sqlite3.connect('MalabuyocDatabase.db')
    cur = con.cursor()

    query = cur.execute(
        "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='data'"
    )

    if query.fetchone()[0] == 1:
        return con, cur
    else:
        cur.execute(
            'CREATE TABLE data(id INTEGER PRIMARY KEY, item TEXT, unit TEXT, price REAL, stock REAL)'
        )
        con.commit()
        return con, cur


def add_record(data):
    con, cur = init_db()
    with con:
        cur.execute(f'INSERT INTO data VALUES(NULL, ?, ?, ?, ?)', data)
        con.commit()


def view_data():
    con, cur = init_db()
    with con:
        cur.execute(f'SELECT * FROM data')
        rows = cur.fetchall()
        con.commit()
    return rows


def delete_record(id):
    con, cur = init_db()
    with con:
        cur.execute('DELETE FROM data WHERE id=?', (id,))
        con.commit()


def search_data(item='', unit=''):
    con, cur = init_db()
    with con:
        if item != '' and unit != '':
            cur.execute(
                'SELECT * FROM data WHERE item=? AND unit=?', (item, unit))
        else:
            cur.execute(
                'SELECT * FROM data WHERE item=? OR unit=?', (item, unit))
        rows = cur.fetchall()
        con.commit()
    return rows


def update_data(id, item='', unit='', price='', stock=''):
    con, cur = init_db()
    with con:
        cur.execute('UPDATE data SET item=?, unit=?, price=?, stock=? WHERE id=?',
                    (item, unit, price, stock, id))
        con.commit()


if __name__ == "__main__":
    print(view_data())
