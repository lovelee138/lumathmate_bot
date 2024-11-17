from db import connect
from random import shuffle


def expand_all_members():
    """In table 'all_members' it counts how many ids were created and generates next 100 ids. It fills gaps:
    'tg_id' = 0;
    'status' = None;
    'name' = None;
    """

    conn, cursor = connect()

    request = f"SELECT rows FROM tables_info WHERE name='all_members';"
    cursor.execute(request)

    counter = cursor.fetchall()[0][0]

    new_ids = [i for i in range(counter + 1, counter + 101)]
    shuffle(new_ids)

    for id in new_ids:
        request = f"INSERT INTO all_members VALUES(0, {id}, 'None', 'None');"
        cursor.execute(request)

        request = f"UPDATE tables_info set rows=rows+1 WHERE name='all_members';"
        cursor.execute(request)

    conn.commit()

    cursor.close()
    conn.close()