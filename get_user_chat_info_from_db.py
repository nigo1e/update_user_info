from db import get_conn
import json
import os
from tqdm import tqdm
def get_full_chat_history_from_db():
    """
    通过数据库连接获取指定外部联系人的所有聊天记录，并构造新的存储格式
    :param external_uid: 外部联系人ID
    :return: 格式化后的聊天记录
    """
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            get_user_ids="""
                select distinct usr.`外部联系人ID`
                from wx_hongniang.`用户` usr
                join wx_hongniang.trace_logs tl
                on usr.`外部联系人ID` = tl.external_userid
                where usr.`外部联系人ID` is not null
                and DATE(usr.`入库时间`) < '2025-04-01' 
                and tl.external_userid is not null
                and tl.trace_tag like '删除%'
            """
            cursor.execute(get_user_ids)
            user_ids = cursor.fetchall()
            users = []
            for uid in tqdm(user_ids):
                uid = uid[0]
                # 查询与外部联系人的所有相关聊天记录
                labels = """
                    SELECT *
                    FROM `用户`
                    WHERE `外部联系人ID` =  %s
                """
                chat_history= """
                    SELECT `from`, content
                    FROM chat_text c
                    WHERE c.`from` = %s OR c.`tolist` LIKE %s
                    ORDER BY c.`msgtime_format`
                """
                cursor.execute(labels, (uid,))
                user_labels = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                user_labels_key = [dict(zip(columns, row)) for row in user_labels]
       
                cursor.execute(chat_history, (uid, f"%{uid}%"))
                chat_records = cursor.fetchall()
                # 构造新的存储格式
                chat_history = []

                for line in chat_records:
                    from_id,content = line
                    # 确定消息角色
                    speaker = "user" if from_id == uid else "assistant"
                    # 添加消息到格式化数据中
                    chat_history.append({
                        "role": speaker,
                        "content": content,
                    })
                # users.append({
                #     "user": uid,
                #     "user_labels": user_labels_key,
                #     "chat_history": chat_history
                # })
                with open(f"chats/{uid}.json", "w", encoding="utf-8") as f:
                    json.dump({
                        "user": uid,
                        "user_labels": user_labels_key,
                        "chat_history": chat_history
                    }, f, ensure_ascii=False, indent=4)
            # return users
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    get_full_chat_history_from_db()
