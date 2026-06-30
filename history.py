# ==========================================定义历史使用数据==========================================
def get_history(cursor, resource, mi=10):
    # 从MySQL查询最近10条的资源历史值
    if not cursor:
        return "无历史数据"
    # 根据resource 选择字段
    sql = f"select timestamp, {resource} from metrics where timestamp > NOW() - interval %s minute order by timestamp limit 100"
    cursor.execute(sql, (mi,))
    rows = cursor.fetchall()
    if not rows:
        return "历史数据为空"
    return "\n".join([f"{r[0]} : {r[1]}%" for r in rows])

# ==========================================定义历史使用数据==========================================
