import psycopg2 as ps
from configparser import ConfigParser
import random
from datetime import datetime


def load_config(filename="./config/database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return config


def connect(config):
    """Connect to the PostgreSQL database server"""
    try:
        # connecting to the PostgreSQL server
        with ps.connect(**config) as conn:
            print("Connected to the PostgreSQL server.")
            return conn, conn.cursor()
    except (ps.DatabaseError, Exception) as error:
        print(error)


def is_signed_up(tg_id: int):
    """In table 'all_members' it tries to find a member with its 'tg_id'.
    Returns member_id, if it was found.
    Else returns False."""

    conn, cursor = connect(load_config())

    request_member_id = f"SELECT member_id FROM all_members WHERE tg_id={tg_id};"
    cursor.execute(request_member_id)

    member_id = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(member_id) == 0:
        return False

    return member_id[0][0]


def expand_all_members():
    """In table 'all_members' it counts how many ids were created and generates next 100 ids. It fills gaps:
    'tg_id' = 0;
    'status' = None;
    'name' = None;
    """

    conn, cursor = connect(load_config())

    request = f"SELECT rows FROM tables_info WHERE name='all_members';"
    cursor.execute(request)

    counter = cursor.fetchall()[0][0]

    new_ids = [i for i in range(counter + 1, counter + 101)]
    random.shuffle(new_ids)

    for id in new_ids:
        request = f"INSERT INTO all_members VALUES(0, {id}, 'None', 'None');"
        cursor.execute(request)

        request = f"UPDATE tables_info set rows=rows+1 WHERE name='all_members';"
        cursor.execute(request)

    conn.commit()

    cursor.close()
    conn.close()


def get_name_by_id(id: int) -> str:
    """It returns name of user by its member-id. If id is not defined then it returns 'None'"""

    conn, cursor = connect(load_config())

    request = f"SELECT name FROM all_members WHERE member_id='{id}';"
    cursor.execute(request)
    name = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(name) == 0:
        return None
    return name[0][0]


def get_status_by_id(id: int) -> str:
    """It returns status of user by its tg-id. If id is not defined in table 'all_members' then it returns 'None'"""

    conn, cursor = connect(load_config())

    request = f"SELECT status FROM all_members WHERE tg_id={id};"
    cursor.execute(request)
    status = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(status) == 0:
        return None
    return status[0][0]


def is_student_member_id_correct(id: int) -> bool:
    """It returns true if member_id connected to any teacher, otherwise it returns false"""

    conn, cursor = connect(load_config())

    request = f"SELECT teacher_id FROM teacher_student WHERE student_id={id};"
    cursor.execute(request)
    teacher_id = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(teacher_id) == 0:
        return False
    return True


def get_new_member_id(status: str) -> int:
    """This function generates new member_id for teachers, new students.
    Status can be 'student' or 'teacher'."""
    conn, cursor = connect(load_config())

    request = f"SELECT * FROM all_members WHERE status='None';"
    cursor.execute(request)

    if len(cursor.fetchall()) == 0:
        expand_all_members()

    request = f"SELECT * FROM all_members WHERE status='None';"
    cursor.execute(request)
    member_ids = cursor.fetchall()

    new_member_id = member_ids[0][1]

    if status == "student" or status == "teacher":
        request = (
            f"UPDATE all_members set status='{status}' WHERE member_id={new_member_id};"
        )
        cursor.execute(request)
        conn.commit()
        cursor.close()
        conn.close()
    else:
        cursor.close()
        conn.clos()
        return None

    return new_member_id


def add_new_member(tg_id, member_id, name, status):
    """This functions updates table 'all_members'."""
    conn, cursor = connect(load_config())

    request = f"UPDATE all_members set tg_id={tg_id}, name='{name}', status='{status}' WHERE member_id={member_id};"
    cursor.execute(request)

    conn.commit()
    cursor.close()
    conn.close()
    return


def get_member_id_by_tg_id(tg_id):
    """This function returns member_id by tg_id"""

    conn, cursor = connect(load_config())
    request = f"SELECT member_id FROM all_members WHERE tg_id='{tg_id}';"
    cursor.execute(request)

    member_id = cursor.fetchall()

    cursor.close()
    conn.close()
    if member_id:
        return member_id[0][0]
    else:
        return False


def is_student_name_correct(name, teacher_tg_id):
    """This function checkes if there is a student with name 'name' for teacher with tg_id 'teacher_tg_id.
    It returns student_id if it's true, else it returns FALSE"""

    teacher_member_id = get_member_id_by_tg_id(teacher_tg_id)
    if not teacher_member_id:
        return False

    conn, cursor = connect(load_config())

    request = f"SELECT student_id FROM teacher_student WHERE teacher_id='{teacher_member_id}' AND name='{name}';"
    cursor.execute(request)

    student_id = cursor.fetchall()
    cursor.close()
    conn.close()

    if student_id:
        return student_id[0][0]
    return False


def get_student_name(student_member_id):
    """This function returns student name (for teacher) by student_member_id"""
    conn, cursor = connect(load_config())

    request = (
        f"SELECT name FROM teacher_student WHERE student_id='{student_member_id}';"
    )
    cursor.execute(request)

    student_name = cursor.fetchall()

    cursor.close()
    conn.close()

    if student_name:
        return student_name[0][0]
    return False


def get_last_note_number(student_member_id):
    """This function returns number of last sent note by student_member_id.
    If student has no any notes, returns 0."""
    conn, cursor = connect(load_config())

    request = (
        f"SELECT last_number FROM number_notes WHERE student_id='{student_member_id}';"
    )
    cursor.execute(request)

    number = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(number) != 0:
        return number[0][0]
    else:
        conn, cursor = connect(load_config())

        request = f"INSERT INTO number_notes VALUES ('{student_member_id}', 0, 0);"
        cursor.execute(request)

        conn.commit()
        cursor.close()
        conn.close()
        return 0


def is_note_number_correct(student_member_id, number):
    """This function finds if there is such note number in table number_notes.
    It returns True, if number_notes is there, else False."""
    conn, cursor = connect(load_config())

    request = f"SELECT number FROM notes_info WHERE student_id='{student_member_id}';"
    cursor.execute(request)

    numbers = list(key[0] for key in cursor.fetchall())

    if number in numbers:
        return True
    return False


def add_new_note(file_name, user_data, path, file_id):
    """This function add new file to notes_info table.
    User_data must be a dict with student_id, date, number, file_id"""
    conn, cursor = connect(load_config())

    request = "INSERT INTO notes_info VALUES('{}', {}, {}, '{}', '{}', '{}');".format(
        file_name,
        user_data["student_id"],
        user_data["number"],
        path,
        file_id,
        user_data["date"],
    )

    cursor.execute(request)

    request = f"UPDATE number_notes SET amount=amount+1, last_number={user_data['number']} WHERE student_id={user_data['student_id']};"

    cursor.execute(request)

    with open(f"{path+file_name}_description.txt", "w") as descr_file:
        descr_file.write(user_data["description"])

    conn.commit()
    cursor.close()
    conn.close()


def get_list_of_notes(student_id: int) -> list:
    """This function return list with note_data for student_id (member_id).
    This notes sorted by date from new to old.
    note_data - dict{"description": <path_to_txt>, "number": n, "date": date, "file_id": file_id, "file_path": <full_path_to_file}
    """
    conn, cursor = connect(load_config())

    request = f"SELECT * from notes_info WHERE student_id='{student_id}';"

    cursor.execute(request)

    notes = cursor.fetchall()
    notes = sorted(notes, key=lambda note: datetime.strptime(note[-1], r"%Y-%m-%d"))

    cursor.close()
    conn.close()
    return notes


def get_all_students(teacher_id: int) -> list:
    """This function return list with student names of teacher."""
    conn, cursor = connect(load_config())

    request = f"SELECT student_id, name FROM teacher_student WHERE \
        teacher_id ={teacher_id};"
    cursor.execute(request)

    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return students
