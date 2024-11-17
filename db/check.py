from db import connect
import get


def signed_up(tg_id: int):
    """In table 'all_members' it tries to find a member with its 'tg_id'.
    Returns member_id, if it was found.
    Else returns False."""

    conn, cursor = connect()

    request_member_id = f"SELECT member_id FROM all_members WHERE tg_id={tg_id};"
    cursor.execute(request_member_id)

    member_id = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(member_id) == 0:
        return False

    return member_id[0][0]


def stud_member_id_correct(id: int) -> bool:
    """It returns true if member_id connected to any teacher, otherwise it returns false"""

    conn, cursor = connect()

    request = f"SELECT teacher_id FROM teacher_student WHERE student_id={id};"
    cursor.execute(request)
    teacher_id = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(teacher_id) == 0:
        return False
    return True


def stud_name_correct(name, id_teac):
    """This function checkes if there is a student with name 'name' for teacher with tg_id 'teacher_tg_id.
    """

    conn, cursor = connect()

    request = f"SELECT student_id FROM teacher_student WHERE teacher_id='{id_teac}' AND name='{name}';"
    cursor.execute(request)

    student_id = cursor.fetchall()
    cursor.close()
    conn.close()

    if student_id:
        return True
    return False


def note_num_correct(id, num):
    """This function finds if there is such note num in table number_notes.
    It returns True, if num_notes is there, else False."""
    conn, cursor = connect()

    request = f"SELECT num FROM notes_info WHERE student_id='{id}';"
    cursor.execute(request)

    nums = list(key[0] for key in cursor.fetchall())

    conn.close()
    cursor.close()
    
    if num in nums:
        return True
    return False