chat_prompt='''
你的任务是根据给定的用户与助手的对话记录，提取用户本人的身份标签和用户对于目标对象的偏好标签，并以JSON字典的格式输出结果。
请按照以下要求提取信息：
1. *本人微信号*：用户的微信号。
2. *抖音号*：用户的抖音号。
3. **本人真名**：用户的真实姓名，格式为中文，5字以内。必须符合中国人起名习惯包括姓氏和名字。
4. **年龄**：用户的年龄，使用用户的年龄或根据用户出生年来计算，只能是两位数字。
5. **学历**：用户的学历。只能是["博士"、"硕士"、"本科"、"大专"、"高中"、"中专"、"初中及以下"]中的一个。
6. **职业**：用户的职业。格式为中文，20字以内。如"程序员"。
7. **收入**：用户的月收入。只能是["2w以上"、"1w - 2w"、"5k - 1w"、"5K以下"]中的一个。
8. **当前坐标**：用户的当前坐标，仅提取最低一级的位置。结果如"北京市"。
9. **现所在地区标签**:根据用户的当前坐标，只能是 ["北京市", "天津市", "上海市", "重庆市", "河北省", "河南省", "山东省", "山西省", "陕西省","吉林省", "黑龙江省", "辽宁省", "内蒙古自治区", "新疆维吾尔自治区","青海省", "甘肃省", "宁夏回族自治区", "四川省", "云南省","贵州省", "湖南省", "湖北省", "江西省", "安徽省","江苏省", "浙江省", "福建省", "广东省", "海南省","广西壮族自治区", "西藏自治区"]中的一个。
10. **身高**：用户的身高。格式为两位或三位数字。如"175"。
11. **体重**：用户的体重，格式为两位数字，单位为kg，体重应在30kg到100kg之间，将斤转化为公斤，结果如"70"。
12. **家乡**：用户的家乡，仅提取最低一级的位置。结果如"北京市"。
13. **爱好**：用户的爱好，格式为中文，20字以内。如"打篮球"。
14. **性格**：用户的性格，格式为中文，20字以内。如"开朗"。
15. **身材**：用户的身材，格式为中文，20字以内。如"匀称"。
16. **气质**：用户的气质，格式为中文，20字以内。如"优雅"。
17. **是否有房**：用户是否有房。只能是["有"、"无"]中的一个。
18. **是否有车**：用户是否有车。只能是["有"、"无"]中的一个。
19. **星座**：用户的星座。只能是["白羊座"、"金牛座"、"双子座"、"巨蟹座"、"狮子座"、"处女座"、"天秤座"、"天蝎座"、"射手座"、"摩羯座"、"水瓶座"、"双鱼座"]中的一个。
20. **MBTI**：用户的MBTI类型。只能是["INTJ"、"INTP"、"ENTJ"、"ENTP"、"INFJ"、"INFP"、"ENFJ"、"ENFP"、"ISTJ"、"ISFJ"、"ESTJ"、"ESFJ"、"ISTP"、"ISFP"、"ESTP"、"ESFP"]中的一个。
21. **自我介绍**：用户的自我介绍，格式为中文，30字以内。如"我是一个程序员，喜欢打篮球"。
22. **目标年龄**：用户的目标对象年龄，年龄的范围。如"20岁以上"，"28岁以下"，"20岁到25岁"等。
23. **目标身高**：用户的目标对象身高，身高的范围。如"175cm以上"，"160cm到175cm"等。
24. **目标爱好**：用户的目标对象爱好，格式为中文，20字以内。如"打篮球"。
25. **目标性格**：用户的目标对象性格，格式为中文，20字以内。如"开朗"。
26. **目标家乡**：用户的目标对象家乡，仅提取最低一级的位置，有多个位置时用“|”分割。结果如"北京市|广东省"。
27. **目标当前坐标**：用户的目标对象当前坐标，仅提取最低一级的位置，有多个位置时用“|”分割。结果如"北京市|广东省"。
28. **目标学历**：用户的目标对象学历，格式为中文，20字以内。学历的范围，如"本科及以上"，"大专"等。
29. **目标收入**：用户的目标对象月收入，只能是["2w以上"、"1w - 2w"、"5k - 1w"、"5K以下"]中的一个。
30. **目标是否有房**：用户的目标对象是否有房。只能是["有"、"无"]中的一个。
31. **目标是否有车**：用户的目标对象是否有车。只能是["有"、"无"]中的一个。
32. **目标身材**：用户的目标对象身材，格式为中文，20字以内。如"匀称"。
33. **目标气质**：用户的目标对象气质，格式为中文，20字以内。如"优雅"。

【注意事项】
1. 如果用户没有提供某个信息，请将其值设置为""。
2. 如果用户提供的信息不符合要求，请将其值设置为""。
3. 请确保输出的JSON格式正确。
4. **区分用户本人 vs 用户期望对象**：
   - 用户描述自己的经历/情况/属性，填入个人字段（如年龄、职业、性格等）
   - 如果用户在回答“你希望对方是……？”、“你对年龄/身高/地域有什么要求？”等助手提问时提到信息，这些应填入“目标对象”字段

【输出格式】请按如下字段严格返回,保证没有其他字段：
{
  "本人微信号": "", "抖音号": "", "本人真名": "", "年龄": "", "学历": "", "职业": "", "收入": "",
  "当前坐标": "","现所在地区标签": "", "身高": "", "体重": "", "家乡": "", "爱好": "", "性格": "",
  "身材": "", "气质": "", "是否有房": "", "是否有车": "", "星座": "",
  "MBTI": "", "自我介绍": "",

  "目标年龄": "", "目标身高": "", "目标爱好": "", "目标性格": "",
  "目标家乡": "", "目标当前坐标": "", "目标学历": "", "目标收入": "",
  "目标是否有房": "", "目标是否有车": "", "目标身材": "", "目标气质": ""
}
'''
example='''
    Q:
    {
        "role": "assistant",
        "content": "你可以接受的年龄范围是什么样子的呀？"
    },
    {
        "role": "user",
        "content": "20-25"
    },
    {
        "role": "assistant",
        "content": "学历和收入有要求吗？"
    },
    {
        "role": "user",
        "content": "学历最好是研究生吧，收入没要求，因为我现在也是研究生，还没有工作呢"
    },
    {
        "role": "assistant",
        "content": "地域有要求吗？"
    },
    {
        "role": "user",
        "content": "没要求，但还是越近越好吧"
    },
    {
        "role": "assistant",
        "content": "还有其他的补充嘛？"
    },
    {
        "role": "user",
        "content": "性格温柔善良，偏御姐型，活泼开朗，身高160+"
    },
    {
        "role": "user",
        "content": "和我差不多的年龄，好看，爱粘人饭"
    },
    {
        "role": "user",
        "content": "和我差不多的年龄，好看，爱做饭，身材好"
    },
    {
        "role": "assistant",
        "content": "学历和收入有要求吗？"
    },
    {
        "role": "user",
        "content": "没有"
    },
    {
        "role": "assistant",
        "content": "地域有要求吗？"
    },
    {
        "role": "user",
        "content": "广西，广州"
    },
    {
        "role": "assistant",
        "content": "还有其他的补充嘛？"
    },
    {
        "role": "user",
        "content": "没有"
    },
    {
        "role": "assistant",
        "content": "按这个格式填下个人资料吧\n称呼：\n年龄：\n身高体重：\n家乡：\n当前坐标：\n学历：\n上学 or 工作情况：\n收入情况：\n兴趣爱好：\n微信号：\n抖音号："
    },
    {
        "role": "user",
        "content": "？？？"
    },
    {
        "role": "assistant",
        "content": "不好意思吓到你啦 这是为了能更精准地给你找到合适的对象哦~现在方便开始填写个人资料嘛"
    }
    A:
    {
    "本人微信号": "", "抖音号": "", "本人真名": "","年龄": "", "学历": "", "职业": "程序员", "收入": "",
    "当前坐标": "","现所在地区标签": "", "身高": "", "体重": "", "家乡": "", "爱好": "", "性格": "",
    "身材": "", "气质": "", "是否有房": "", "是否有车": "", "星座": "",
    "MBTI": "", "自我介绍": "",

    "目标年龄": "20到25", "目标身高": "大于160", "目标爱好": "爱做饭", "目标性格": "性格温柔善良，活泼开朗",
    "目标家乡": "", "目标当前坐标": "广西|广州", "目标学历": "硕士", "目标收入": "",
    "目标是否有房": "", "目标是否有车": "", "目标身材": "身材好", "目标气质": "，偏御姐型"
    }
'''
from openai import OpenAI
import json
import jionlp as jio
import pandas as pd
from datetime import datetime
class UserLabelsExtractor:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key="2a5364ab-5afa-4639-932c-b915d0ee4ade",
        )
        self.ageTag = ["00后", "95后", "90后", "85后", "80后"]
        # 年龄标签对应的出生年份阈值：2000+, 1995-1999, 1990-1994, 1985-1989, 1980-1984
        self.ageThresholds = [2000, 1995, 1990, 1985, 1980]

    def parse_location(self, location):
        """
        仅保留符合 'xx省-xx市-xx县/区' 的格式，多地用 | 分隔
        """
        if not location or pd.isna(location):
            return ''
        
        # 处理列表或字符串类型
        if isinstance(location, list):
            locations = location
        else:
            locations = location.split('|')
        
        ans = []
        for loc in locations:
            if not loc or not isinstance(loc, str):
                continue
                
            loc = loc.strip()
            parsed = jio.parse_location(loc)
            province = parsed.get('province', '')
            city = parsed.get('city', '')
            county = parsed.get('county', '') 
            formatted = '-'.join([p for p in [province, city, county] if p])
            if formatted:  # 确保格式化后不为空
                ans.append(formatted)

        return '|'.join(ans)

    def get_age_label(self, age_str):
        """
        根据年龄字符串计算年龄标签
        使用阈值计算法匹配出生年份对应的标签
        """
        if not age_str:
            return ""
            
        try:
            age = int(age_str)
        except ValueError:
            return ""
            
        current_year = datetime.now().year
        birth_year = current_year - age
        
        # 检查年龄是否在合理范围
        if birth_year < 1900 or birth_year > current_year:
            return ""
        
        # 根据出生年份匹配标签
        for i, th in enumerate(self.ageThresholds):
            if birth_year >= th:
                return self.ageTag[i]
                
        return ""  # 如果年份太早，则返回空

    def extract_user_labels(self, context):
        context_str = json.dumps(context, ensure_ascii=False)
        messages = [
            {"role": "system", "content": chat_prompt},
            {"role": "assistant", "content": example},
            {"role": "user", "content": context_str},
        ]
        
        try:
            completion = self.client.chat.completions.create(
                model="ep-20250424162632-mbdnk",
                messages=messages,
            )
            result = completion.choices[0].message.content
            parsed_json = json.loads(result)
            
            # 直接保留学历和收入标签
            parsed_json["学历标签"] = parsed_json.get("学历", "")
            parsed_json["收入标签"] = parsed_json.get("收入", "")
            
            # 计算年龄标签
            age_str = parsed_json.get("年龄", "")
            parsed_json["年龄标签"] = self.get_age_label(age_str)
            
            # 处理所有地理字段
            for loc_field in ["家乡", "当前坐标", "目标家乡", "目标当前坐标"]:
                val = parsed_json.get(loc_field, '')
                parsed_json[loc_field] = self.parse_location(val)
                
            return parsed_json
            
        except json.JSONDecodeError as decode_err:
            print("chat_response 字符串不是有效的 JSON，错误如下：", decode_err)
            return {}
        except Exception as e:
            print(f"处理过程中发生错误: {str(e)}")
            return {}
if __name__ == '__main__':  
    extractor = UserLabelsExtractor()
    chat_history=[
        {
            "role": "user",
            "content": "我已经添加了你，现在我们可以开始聊天了。"
        },
        {
            "role": "assistant",
            "content": "哈喽哇😁，你是想脱单还是找搭子呢？"
        },
        {
            "role": "assistant",
            "content": "嗨呀，你要找个多大的哈？"
        }
    ]
    labels = extractor.extract_user_labels(chat_history)
    print(json.dumps(labels, ensure_ascii=False, indent=4))  # 打印提取的用户标签
