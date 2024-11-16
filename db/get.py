from db import connect


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

#refactoring
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

    if student_name:
        return student_name[0][0]
    return False