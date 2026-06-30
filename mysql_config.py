def insert_data(cursor, conn, data):
    # ==========================================插入数据==========================================
    sql = """
                insert into metrics 
                (timestamp, cpu_usage, memory_usage, disk_usage, disk_read_mb, disk_write_mb, disk_read_count,
                disk_write_count, net_send_mb, net_resv_mb)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

    # 执行修改参数
    cursor.execute(sql, (
        data['timestamp'], data['cpu_use'], data['free_use'], data['disk_use'],
        data['disk_io_read'], data['disk_io_write'],
        data['disk_io_read_count'], data['disk_io_write_count'],
        data['network_send_b'], data['network_resv_b']
    ))
    conn.commit()  # 用来确认更改

    # 清理数据
    if cursor.lastrowid % 127 == 0:
        cursor.execute("truncate table metrics")
        conn.commit()
        print("数据超过127条，执行清除")
