from ai import UserLabelsExtractor
from check_user_info import check_user_info
import json
import os
from multiprocessing import Pool

# 定义处理单个文件的函数
def process_file(filename):
    extractor = UserLabelsExtractor()
    file_path = os.path.join("chats", filename)
    
    try:
        # 读取用户数据
        with open(file_path, "r", encoding="utf-8") as f:
            user = json.load(f)
        
        chat_history = user.get("chat_history", [])
        if not chat_history:
            print(f"聊天记录为空：{filename}")
            return
        
        # 转换聊天记录为 JSON 字符串
        chat_history_json = json.dumps(chat_history, ensure_ascii=False)
        
        # 提取用户标签
        ans_labels = extractor.extract_user_labels(chat_history_json)
        
        # 检查提取的标签是否符合要求
        if check_user_info(ans_labels):
            ans = {
                "user": user["user"],
                "user_labels": user["user_labels"],
                "ans_user_labels": ans_labels,
                "chat_history": chat_history
            }
            
            # 写入结果到目标文件
            output_path = os.path.join("chat_ans", filename)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(ans, f, ensure_ascii=False, indent=4)
            print(f"处理完成：{filename}")
        else:
            print(f"用户标签不符合要求：{filename}")
    except Exception as e:
        print(f"处理文件 {filename} 时出错：{e}")

if __name__ == "__main__":
    # 获取文件列表
    file_list = os.listdir("chats")
    
    # 确保目标目录存在
    os.makedirs("chat_ans", exist_ok=True)
    
    # 使用多进程处理文件
    with Pool(processes=4) as pool:  # 使用 4 个进程
        pool.map(process_file, file_list)