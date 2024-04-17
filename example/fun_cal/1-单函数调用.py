import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

sys_content=("你是一个精准的格式化信息阅读器，请从相关内容中结构化提取信息，包括："
             "城市：一个城市的名称, 简称：一个城市的简称，别称：城市的其它称呼，面积：总的面积，人员：常住人口数")
usr_content1=("北京市（Beijing），简称“京”，古称燕京、北平，是中华人民共和国首都、直辖市、国家中心城市、超大城市，"
            "国务院批复确定的中国政治中心、文化中心、国际交往中心、科技创新中心，中国历史文化名城和古都之一，世界一线城市。"
            "截至2023年10月，北京市下辖16个区，总面积16410.54平方千米。 2023年末，北京市常住人口2185.8万人。")
usr_content2=("上海市，简称“沪”，别称“申”，中华人民共和国直辖市、国家中心城市、超大城市、上海大都市圈核心城市、国家历史文化名城 ，是中国共产党诞生地。"
            "上海市入围世界Alpha+城市，基本建成国际经济、金融、贸易、航运中心，形成具有全球影响力的科技创新中心基本框架。"
            "截至2023年10月，上海市下辖16个区，总面积6340.5平方千米，市人民政府驻黄浦区人民大道200号。"
            "截至2023年，上海市常住人口为2487.45万人。")
usr_content3=("深圳市，简称“深”，别称鹏城，广东省辖地级市、副省级市、国家计划单列市，超大城市，国务院批复确定的经济特区、全国性经济中心城市和国家创新型城市，"
            "粤港澳大湾区核心引擎城市之一 。截至2022年末，全市下辖9个区，总面积1997.47平方千米，常住人口1766.18万人。")

def context_format_extract(name, abbr, nickname, area, population):
  '''In context format extract'''
  print("In context_format_extract")
  print("City:{}\n"
        "Abbr:{}\n"
        "Nickname:{}\n"
        "Area:{}\n"
        "Population:{}\n".format(name, abbr, nickname, area, population))

tools = [
  {
    "type": "function",
    "function": {
      "name": "context_format_extract",
      "description": "Get the current weather in a given location",
      "parameters":{
        "type": "object",
        "properties":{
          "City":{
            "type": "string",
            "description": "The name of the city"
          },
          "Abbr":{
            "type": "string",
            "description": "Abbreviation of the city name"
          },
          "Nickname":{
            "type": "string",
            "description": "Nickname of the city"
          },
          "Area":{
            "type": "number",
            "description": "Total area of the city"
          },
          "Population":{
            "type": "number",
            "description": "Number of population living in the city"
          }
        }
      }
    }
  }
]

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    #{"role": "system", "content": sys_content},
    {"role": "user", "content": usr_content1},
    {"role": "user", "content": usr_content2},
    {"role": "user", "content": usr_content3},
  ],
  tools = tools,
  tool_choice="auto"
)

for func in response.choices[0].message.tool_calls:
  func_name = func.function.name
  if func_name == "context_format_extract":
    args = func.function.arguments
    print("args:{}".format(args))
    args = json.loads(args)
    context_format_extract(*list(args.values()))