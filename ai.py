import os
from openai import OpenAI
import json
import jionlp as jio
import pandas as pd
import re
from prompt import chat_prompt, example

os.environ["OPENAI_API_KEY"] = "2a5364ab-5afa-4639-932c-b915d0ee4ade"

class UserLabelsExtractor:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

    def parse_location(self, location):
        """
        仅保留符合 'xx省-xx市-xx县/区' 的格式，多地用 | 分隔
        """
        if not location or pd.isna(location):
            return ''
        
        # 合法地名格式：省-市-县/区（支持多组，用 | 分隔）

        locations = location.split('|')
        ans = []
        for loc in locations:
            loc = loc.strip()
            if not loc:
                continue

            parsed = jio.parse_location(loc)
            province = parsed.get('province', '')
            city = parsed.get('city', '')
            county = parsed.get('county', '') 
            formatted = '-'.join([p for p in [province, city, county] if p])
            ans.append(formatted)

        return '|'.join(ans)

    def extract_user_labels(self, context):
        messages = [
            {"role": "system", "content": chat_prompt},
            {"role": "assistant", "content": example},
            {"role": "user", "content": context},
        ]
        completion = self.client.chat.completions.create(
            model="ep-20250424162632-mbdnk",
            messages=messages,
        )
        result = completion.choices[0].message.content
        try:
            parsed_json = json.loads(result)
            for loc_field in ["家乡", "当前坐标", "目标家乡", "目标当前坐标"]:
                val = parsed_json.get(loc_field, '')
                if isinstance(val, str):
                    parsed_json[loc_field] = self.parse_location(val)
                else:
                    print(f"{loc_field} 格式错误，已清空")
                    parsed_json[loc_field] = ''
        except json.JSONDecodeError as decode_err:
            print("chat_response 字符串不是有效的 JSON，错误如下：", decode_err)
            parsed_json = {}
        return parsed_json
