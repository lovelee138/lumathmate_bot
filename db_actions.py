import psycopg2 as ps
from configparser import ConfigParser


def load_config(filename='./config/database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config


def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with ps.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn, conn.cursor()
    except (ps.DatabaseError, Exception) as error:
        print(error)


def get_last_note(student_id):
    connection, cursor = connect(load_config())

    request_last_note = f"SELECT * FROM notes_id WHERE student_id={student_id} ORDER BY date;"
    cursor.execute(request_last_note)
    note_name = f"{cursor.fetchall()[-1][0]}.pdf"
    return note_name


def get_students(teacher_username):
    connection, cursor = connect(load_config())

    request_students = f"SELECT student_username FROM students WHERE teacher_username='{teacher_username}';"
    cursor.execute(request_students)
    students_usernames = []
    for student in cursor.fetchall():
        students_usernames.append(student[0])

    return students_usernames


    