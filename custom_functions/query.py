# Use this to update a row dynamically using SQL Alchemy
def dynamic_update(database_conn, table, request):
    for key, value in request:
        if hasattr(table, key) and value:
            setattr(table, key, value)
    database_conn.commit()
