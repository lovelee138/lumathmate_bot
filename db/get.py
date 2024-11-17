from db import connect
import check
from datetime import datetime
from other import expand_all_members

def member_id(tg_id: int) -> int:
    """It returns status of user by its tg-id. If tg-id is not defined in table 'all_members' then it raises an Exception."""

    conn, cursor = connect()

    request = f"SELECT status FROM all_members WHERE tg_id={id};"
    cursor.execute(request)
    status = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(status) == 0:
        raise Exception(
            f"There's no member with tg-id={tg_id}"
        )
    return status[0][0]


def name_by_id(id: int) -> str:
    """It returns name of user by its member-id. If id is not defined then it raises an Exception."""

    conn, cursor = connect()

    request = f"SELECT name FROM all_members WHERE member_id='{id}';"
    cursor.execute(request)
    name = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(name) == 0:
        raise Exception(
            f"There's no member with member-id={id}"
        )
    return name[0][0]


def status_by_id(id: int) -> str:
    """It returns status of user by its member-id. If id is not defined in table 'all_members' then it raises an Exception"""

    conn, cursor = connect()

    request = f"SELECT status FROM all_members WHERE member_id={id};"
    cursor.execute(request)
    status = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(status) == 0:
        raise Exception(
            f"There's no member with member-id={id}"
        )
    return status[0][0]


def student_name(id_teac: int, id_stud: int) -> str:
    """This function returns student name (for teacher) by student_member_id"""
    conn, cursor = connect()

    request = (
        f"SELECT name FROM teacher_student WHERE student_id='{id_stud} AND teacher_id='{id_teac}';"
    )
    cursor.execute(request)

    student_name = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(student_name) == 0:
        raise Exception(
            f"Teacher with member-id={id_teac} doesn't have student with member-id={id_stud}"
        )
    return student_name[0][0]


def last_note_number(id):
    """This function returns number of last sent note by student's member_id."""
    conn, cursor = connect()

    request = (
        f"SELECT last_number FROM number_notes WHERE student_id='{id}';"
    )
    cursor.execute(request)

    number = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(number) != 0:
        return number[0][0]
    else:
        conn, cursor = connect()

        request = f"INSERT INTO number_notes VALUES ('{id}', 0, 0);"
        cursor.execute(request)

        conn.commit()
        cursor.close()
        conn.close()
        return 0


def get_list_of_notes(id_stud: int) -> list:
    """This function return list with note_data for student by member_id.
    This notes sorted by date from new to old.
    note_data - dict{"description": <path_to_txt>, "number": n, "date": date, "file_id": file_id, "file_path": <full_path_to_file}.
    If there're no notes for this student, it raises an exception.
    """
    conn, cursor = connect()

    request = f"SELECT * from notes_info WHERE id_stud='{id_stud}';"

    cursor.execute(request)

    notes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    if len(notes) == 0:
        raise Exception(
            f"There're no notes for student with member-id={id_stud}"
        )

    notes = sorted(notes, key=lambda note: datetime.strptime(note[-1], r"%Y-%m-%d"))

    return notes


def all_students(id_teac: int) -> list:
    """This function return list with student names of teacher."""
    conn, cursor = connect()

    request = f"SELECT student_id, name FROM teacher_student WHERE \
        id_teac ={id_teac};"
    cursor.execute(request)

    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return students


def new_member_id(status: str) -> int:
    """This function generates new member_id for teachers, new students.
    Status can be 'student' or 'teacher'."""
    conn, cursor = connect()

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
        conn.close()
        raise Exception(
            f"Incorrect status={status}"
        )

    return new_member_id


def member_id_by_name(name, id_teac):
    """This function returns student's member_id by name (for teacher) for teacher with member-id=id_teac.
    If it's not correct name, it raises an Exception."""
 
    conn, cursor = connect()

    request = f"SELECT student_id FROM teacher_student WHERE teacher_id='{id_teac}' AND name='{name}';"
    cursor.execute(request)

    student_id = cursor.fetchall()
    cursor.close()
    conn.close()

    if student_id:
        return student_id[0][0]
    return False