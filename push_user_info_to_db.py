import os
import json
from db import get_conn
from check_user_info import check_user_info

info_path = "chats"
failed_users_file = "failed_users.txt"

def log_failure(user_id, message):
    with open(failed_users_file, "a", encoding="utf-8") as f:
        f.write(f"{user_id}: {message}\n")

def main():
    try:
        conn = get_conn()
    except Exception as e:
        log_failure("数据库连接", f"连接失败: {e}")
        return

    index = 1
    for filename in os.listdir(info_path):
        filepath = os.path.join(info_path, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                user_info = json.load(f)

            if not user_info:
                log_failure(filename, "用户信息为空")
                print(f"{filename}: 用户信息为空")
                continue

            user_id = user_info.get("user")
            update_info = user_info.get("ans_user_labels")

            if not user_id:
                log_failure(filename, "缺少 user_id")
                print(f"{filename}: 缺少 user_id")
                continue

            if not update_info:
                log_failure(user_id, "用户信息无需更新")
                print(f"用户 {user_id} 没有需要更新的信息")
                continue

            if not check_user_info(update_info):
                log_failure(user_id, "用户信息不合法")
                print(f"用户 {user_id} 信息不合法")
                continue

            print(f"\n{index}. 正在更新用户 {user_id} 信息...")
            index += 1

            # 构建 SQL
            update_fields = ", ".join([f"`{key}` = %s" for key in update_info])
            update_values = list(update_info.values()) + [user_id]

            sql = f"""
                UPDATE `用户`
                SET {update_fields}
                WHERE `外部联系人ID` = %s
            """

            with conn.cursor() as cursor:
                cursor.execute(sql, update_values)
            conn.commit()
            print(f"用户 {user_id} 信息更新成功")

        except Exception as e:
            uid = user_info.get("user", filename)
            log_failure(uid, str(e))
            print(f"用户 {uid} 信息更新失败: {e}")

    conn.close()

if __name__ == "__main__":
    main()
