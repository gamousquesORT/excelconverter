def select_split_char_unnamed():
    global value , split_char , split_column
    for value in row.values:
        if value in valid_columns_to_split.keys():
            split_char = valid_columns_to_split[value]
            split_column = str(value)
            break


def insert_course_session_unnamed():
    global inscriptos , cupos
    inscriptos , cupos = df.iloc[row_index , 6].split(split_char)
    # Add Inscriptos and Cupos columns to the row
    row['Inscriptos'] = inscriptos.strip()  # remove leading/trailing spaces
    row['Cupos'] = cupos.strip()
    row['Fecha'] = date_to_insert.strip()  # remove leading/trailing spaces
    # Append the row to the filtered_rows list
    filtered_rows.append(row)


"""
            if 'Materia' in df.columns and not materia_marker_found:
                materia_marker_found = True
                named_column_mode = True

                set_date_to_insert_named()
                select_split_char_named()

                nombre_materia = row['Materia']
                if nombre_materia.strip() in materia_list:
                    try:
                        insert_course_session_named()
                        row_index = row_index + 1
                    except ValueError:
                        # If splitting fails, print a message and continue iterating
                        print("Cannot split Ins_Cupos value in row:" , index)
                        break


            if 'Materia' in row.values and not materia_marker_found:
                materia_marker_found = True
                named_column_mode = False

                select_split_char_unnamed()
                row_index = row_index + 1
                continue


            if named_column_mode is False and materia_marker_found:
                    if is_string(df.iloc[row_index, 3]):
                        nombre_materia = df.iloc[row_index , 3]
                        if nombre_materia.strip() in materia_list:
                            try:
                                insert_course_session_unnamed()
                            except ValueError:
                                # If splitting fails, print a message and continue iterating
                                print("Cannot split Ins_Cupos value in row:" , index)
                                break
                    row_index = row_index + 1
"""