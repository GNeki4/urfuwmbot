import sqlite3


def create_users_table():
    conn = sqlite3.connect('tgbot_dataset.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE users '
                   '(id integer, tgname text, realname text, room integer, is_admin integer)')
    cursor.close()


def add_user(id, tgname, realname, room, is_admin):
    conn = sqlite3.connect('tgbot_dataset.db')
    cursor = conn.cursor()
    row = (id, tgname, realname, room, is_admin)
    sql = """INSERT INTO users (id, tgname, realname, room, is_admin) VALUES (?, ?, ?, ?, ?);"""
    cursor.execute(sql, row)
    conn.commit()
    cursor.close()


def update_user_realname(id, realname):
    conn = sqlite3.connect('tgbot_dataset.db')
    cursor = conn.cursor()
    sql = 'Update users set realname = ? where id = ?'
    data = (realname, id)
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()


def update_user_room(id, room):
    conn = sqlite3.connect('tgbot_dataset.db')
    cursor = conn.cursor()
    sql = 'Update users set room = ? where id = ?'
    data = (room, id)
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()


def get_user_info(id):
    conn = sqlite3.connect('tgbot_dataset.db')
    cursor = conn.cursor()
    sql = 'SELECT * FROM users WHERE id=?'
    cursor.execute(sql, (id, ))
    try:
        data = list(cursor.fetchall()[0])
        default = ['id', 'tgname', 'realname', 'room', 'is_admin']
        reply = {}
        for i in range(len(data)):
            reply[default[i]] = data[i]
        return reply
    finally:
        cursor.close()


def delete_user_info(id):
    conn = sqlite3.connect('tgbot_dataset.db')
    cursor = conn.cursor()
    sql = 'DELETE FROM users WHERE id=?'
    cursor.execute(sql, (id, ))
    conn.commit()
    cursor.close()


def get_all_ids_and_names():
    conn = sqlite3.connect('tgbot_dataset.db')
    cursor = conn.cursor()
    sql = 'SELECT id, realname FROM users'
    cursor.execute(sql)

    try:
        data = cursor.fetchall()
        default = ['id', 'realname']
        reply = []

        for i in range(len(data)):
            temp = {}
            for j in range(0, 2):
                temp.update({default[j]: data[i][j]})
            reply.append(temp)
        return reply
    finally:
        cursor.close()


def get_specific_ids_and_names(names):
    input_names = names.split("\n")
    print(names)
    conn = sqlite3.connect('tgbot_dataset.db')
    cursor = conn.cursor()
    sql = 'SELECT id, realname FROM users WHERE realname = ?'

    try:
        default = ['id', 'realname']
        reply = []

        for name in input_names:
            cursor.execute(sql, (name, ))
            data = cursor.fetchall()

            for i in range(len(data)):
                temp = {}
                for j in range(0, 2):
                    temp.update({default[j]: data[i][j]})
                reply.append(temp)

        return reply
    finally:
        cursor.close()


# conn = sqlite3.connect('tgbot_dataset.db')
# cursor = conn.cursor()
# cursor.execute('DROP TABLE users;')
# create_users_table()

# print(get_user_info(509365786))

# test = get_all_ids_and_names()
# for i in range(len(test)):
#     print(test[i])
# print("------------------")
# print(test[0]['id'])
# print(test[0]['realname'])

#test = get_specific_ids_and_names("Печков Н.В.\nМустафина Л.А.")
#print(test)
