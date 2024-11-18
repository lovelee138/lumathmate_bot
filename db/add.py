from db import connect


def new_member(tg_id, member_id, name, status):
    """This functions updates table 'all_members'."""
    conn, cursor = connect()

    request = f"UPDATE all_members set tg_id={tg_id}, name='{name}', status='{status}' WHERE member_id={member_id};"
    cursor.execute(request)

    conn.commit()
    cursor.close()
    conn.close()
    return


def new_note(file_name, note_data, path):
    """This function add new file to notes_info table.
    Note_data must be a dict with student_id, date, number, file_id"""
    conn, cursor = connect()

    request = "INSERT INTO notes_info VALUES('{}', {}, {}, '{}', '{}', '{}');".format(
        file_name,
        note_data["student_id"],
        note_data["number"],
        path,
        note_data["file_id"],
        note_data["date"],
    )

    cursor.execute(request)

    request = f"UPDATE number_notes SET amount=amount+1, last_number={note_data['number']} WHERE student_id={note_data['student_id']};"

    cursor.execute(request)

    with open(f"{path+file_name}_description.txt", "w") as descr_file:
        descr_file.write(note_data["description"])

    conn.commit()
    cursor.close()
    conn.close()


def new_student(id_stud, id_teac, name):
    """This function adds note (student_id, teacher_id, name(student)) in table 'teacher_student'"""

    conn, cursor = connect()

    request = f"INSERT INTO teacher_student VALUES({id_stud}, {id_teac}, '{name}');"
    cursor.execute(request)

    conn.commit()
    cursor.close()
    conn.close()
