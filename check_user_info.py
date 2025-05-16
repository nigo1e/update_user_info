import re
def check_user_info(user_info):
    print("用户信息:", user_info)
    if not isinstance(user_info, dict):
        print("用户信息格式错误")
        return False
    if user_info == {}:
        print("用户信息为空")
        return False
    required_fields = [
        "本人微信号", "抖音号", "本人真名", "年龄", "学历", "职业", "收入","当前坐标", "身高", "体重", 
        "家乡", "爱好", "性格","身材","气质", "是否有房", "是否有车", "星座","MBTI", "自我介绍", 
        "目标年龄","目标身高", "目标爱好", "目标性格","目标家乡", "目标当前坐标", "目标学历", "目标收入","目标是否有房", "目标是否有车",
        "目标身材", "目标气质"
    ]
    if len(user_info) != len(required_fields):
        print("用户信息字段错误")
        return False
    for field in required_fields:
        if field not in user_info:
            print(f"缺少字段: {field}")
            return False

    #1.
    if user_info["本人微信号"] !="" and not re.match(r"^[^\u4e00-\u9fff]{6,20}$", user_info["本人微信号"]):
        print("微信号格式错误")
        user_info["本人微信号"] = ""
    #2.
    #2.
    if user_info["抖音号"] !="" and not re.match(r"^[^\u4e00-\u9fff\s]{3,30}$", user_info["抖音号"]):  # 允许3~30字符的非中文非空格
        print("抖音号格式错误")
        user_info["抖音号"] = ""
    #3.
    if user_info["本人真名"] !="" and not re.match(r"^[\u4e00-\u9fa5]{2,10}$", user_info["本人真名"]):
        print("姓名格式错误")
        user_info["本人真名"] = ""
    #4.
    if user_info["年龄"] !="" and not re.match(r"^\d{1,3}$", user_info["年龄"]):
        print("年龄格式错误")
        user_info["年龄"] = ""
    #5.
    if user_info["学历"] !="" and user_info["学历"] not in ["博士", "硕士", "本科", "大专", "高中", "中专", "初中及以下"]:
        print("学历格式错误")
        user_info["学历"] = ""
    #6.
    # if user_info["职业"] !="" and not re.match(r"^[\u4e00-\u9fa5]{2,10}$", user_info["职业"]):
    #     print("职业格式错误")
    #     user_info["职业"] = ""
    #7.
    if user_info["收入"] !="" and user_info["收入"] not in ["2w以上", "1w - 2w", "5k - 1w", "5K以下"]:
        print("收入格式错误")
        user_info["收入"] = ""  
    #8.
    # if user_info["当前坐标"] !="" and not re.match(r"^([\u4e00-\u9fa5]{2,10}省|[\u4e00-\u9fa5]{2,10}市)-[\u4e00-\u9fa5]{2,10}市-[\u4e00-\u9fa5]{2,10}(县|区)$", user_info["当前坐标"]):
    #     print("当前坐标格式错误")
    #     user_info["当前坐标"] = ""  
    #9.
    if user_info["身高"] !="" and not re.search(r"^\d{1,3}$", user_info["身高"]):
        print("身高格式错误")
        user_info["身高"] = ""
    #10.
    if user_info["体重"] !="" and not re.search(r"^\d{1,3}$", user_info["体重"]):
        print("体重格式错误")
        user_info["体重"] = ""
    # #11.
    # if user_info["家乡"] != "" and not re.match(r"^([\u4e00-\u9fa5]{2,10}省|[\u4e00-\u9fa5]{2,10}市)-[\u4e00-\u9fa5]{2,10}市-[\u4e00-\u9fa5]{2,10}(县|区)$", user_info["家乡"]):
    #     print("家乡格式错误")
    #     user_info["家乡"] = ""  

    def check_chinese_field(name, value):
        value = value.strip()
        if value !="" and not (1 <= len(value) < 30):
            print(f"{name}格式错误")
            return False
        return True
    #12.13.14.15.16.17.18.19.20
    for field in ["爱好", "性格", "身材", "气质","自我介绍", "目标爱好", "目标性格", "目标身材", "目标气质","目标学历","职业"]:
        if not check_chinese_field(field, user_info[field]):
            print(f"{field}格式错误")
            user_info[field] = ""
    #匹配是否包含数字
    if user_info["目标年龄"] != "" and not re.search(r"\d", user_info["目标年龄"]):
        print("目标年龄格式错误")
        user_info["目标年龄"] = ""

    if user_info["目标身高"] !="" and not re.search(r"\d", user_info["目标身高"]):
        print("目标身高格式错误")
        user_info["目标身高"] = ""
    #21.
    if user_info["是否有房"] !="" and user_info["是否有房"] not in ["有", "无"]:
        print("是否有房格式错误")
        user_info["是否有房"] = ""
    #22.
    if user_info["是否有车"] !="" and user_info["是否有车"] not in ["有", "无"]:
        print("是否有车格式错误")
        user_info["是否有车"] = ""
    #23.
    zodiac_list = ["白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座",
                   "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座"]
    if user_info["星座"] !="" and user_info["星座"] not in zodiac_list:
        print("星座格式错误")
        user_info["星座"] = ""  
    #24.

    mbti_list=["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
    if user_info["MBTI"] !="" and user_info["MBTI"] not in mbti_list:
        print("MBTI格式错误")
        user_info["MBTI"] = ""
    #25.
    # if user_info["目标家乡"] !="" and not re.match(r"^([\u4e00-\u9fa5]{2,20}(省|市)(-[\u4e00-\u9fa5]{2,10}市)?(-[\u4e00-\u9fa5]{2,10}(县|区))?)(\|[\u4e00-\u9fa5]{2,10}(省|市)(-[\u4e00-\u9fa5]{2,10}市)?(-[\u4e00-\u9fa5]{2,10}(县|区))?)*$", user_info["目标家乡"]):
    #     print("目标家乡格式错误")
    #     user_info["目标家乡"] = ""
    # #28.
    # if user_info["目标当前坐标"] !="" and not re.match(r"^([\u4e00-\u9fa5]{2,10}(省|市)(-[\u4e00-\u9fa5]{2,10}市)?(-[\u4e00-\u9fa5]{2,10}(县|区))?)(\|[\u4e00-\u9fa5]{2,10}(省|市)(-[\u4e00-\u9fa5]{2,10}市)?(-[\u4e00-\u9fa5]{2,10}(县|区))?)*$", user_info["目标当前坐标"]):
    #     print("目标当前坐标格式错误")
    #     user_info["目标当前坐标"] = ""  
    #30.
    if user_info["目标收入"] !="" and user_info["目标收入"] not in ["2w以上", "1w - 2w", "5k - 1w", "5K以下"]:
        print("收入格式错误")
        user_info["目标收入"] = ""
    #31.
    if user_info["目标是否有房"] !="" and user_info["目标是否有房"] not in ["有", "无"]:
        print("目标是否有房格式错误")
        user_info["目标是否有房"] = ""
    #32.
    if user_info["目标是否有车"] !="" and user_info["目标是否有车"] not in ["有", "无"]:
        print("目标是否有车格式错误")
        user_info["目标是否有车"] = ""
    return True