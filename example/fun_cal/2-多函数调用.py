import os
import json
import requests
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

sys_content=("无论给你什么样的问题，你先回答问题，然后尽量的发起函数调用")
usr_content1=("北京市（Beijing），简称“京”，古称燕京、北平，是中华人民共和国首都、直辖市、国家中心城市、超大城市，"
            "国务院批复确定的中国政治中心、文化中心、国际交往中心、科技创新中心，中国历史文化名城和古都之一，世界一线城市。"
            "截至2023年10月，北京市下辖16个区，总面积16410.54平方千米。 2023年末，北京市常住人口2185.8万人。")
usr_content2=("上海市，简称“沪”，别称“申”，中华人民共和国直辖市、国家中心城市、超大城市、上海大都市圈核心城市、国家历史文化名城 ，是中国共产党诞生地。"
            "上海市入围世界Alpha+城市，基本建成国际经济、金融、贸易、航运中心，形成具有全球影响力的科技创新中心基本框架。"
            "截至2023年10月，上海市下辖16个区，总面积6340.5平方千米，市人民政府驻黄浦区人民大道200号。"
            "截至2023年，上海市常住人口为2487.45万人。")
usr_content3=("深圳市，简称“深”，别称鹏城，广东省辖地级市、副省级市、国家计划单列市，超大城市，国务院批复确定的经济特区、全国性经济中心城市和国家创新型城市，"
            "粤港澳大湾区核心引擎城市之一 。截至2022年末，全市下辖9个区，总面积1997.47平方千米，常住人口1766.18万人。")
usr_content4=("中国的首都在哪儿？告诉我它的天气")

def context_format_extract(name, abbr, nickname, area, population):
  '''In context format extract'''
  print("In context_format_extract")
  print("City:{}\n"
        "Abbr:{}\n"
        "Nickname:{}\n"
        "Area:{}\n"
        "Population:{}\n".format(name, abbr, nickname, area, population))


def get_location_weather(location="北京", extensions="base", output="json"):
  '''GAODE weather API'''
  city_code = { "北京": 110000, "上海": 310000, "广州": 440100, "深圳": 440300}
  citycode = city_code.get(location)
  if citycode == None:
    citycode = 11000

  # 发送GET请求
  API_URL = "https://restapi.amap.com/v3/weather/weatherInfo"
  params = {"key": os.environ['GAODE_API_KEY'], "city": citycode, "extensions": extensions, "output": output}
  response = requests.get(API_URL, params=params)
  # print(response.url)
  weather_info = response.json()
  print("{}的实时天气情况：".format(location))
  print("天气：{}".format(weather_info['lives'][0].get('weather')))
  print("气温：{}".format(weather_info['lives'][0].get('temperature')))
  print("风向：{}".format(weather_info['lives'][0].get('winddirection')))
  print("风力：{}".format(weather_info['lives'][0].get('windpower')))
  print("温度：{}".format(weather_info['lives'][0].get('humidity')))
  print("消息更新时间：{}".format(weather_info['lives'][0].get('reporttime')))

tools = [
  {
    "type": "function",
    "function": {
      "name": "context_format_extract",
      "description": "Get the format information",
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
  },
  {
    "type": "function",
    "function": {
      "name": "get_location_weather",
      "description": "Get the current weather in a given location",
      "parameters":{
        "type": "object",
        "properties":{
          "location":{
            "type": "string",
            "description": "The name of the city, or county or district"
          },
          "extensions":{
            "type": "string",
            "description": "'base' returns realtime weather, 'all' returns weather forecast"
          },
          "output":{
            "type": "string",
            "description": "JSON or XML"
          },
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
    {"role": "user", "content": usr_content4},
  ],
  tools = tools,
  tool_choice="auto"
)

print(response.choices[0].message.content)

for func in response.choices[0].message.tool_calls:
  func_name = func.function.name
  func_dict = {"context_format_extract": context_format_extract,
             "get_location_weather": get_location_weather}

  func_call = func_dict.get(func_name)
  args = func.function.arguments
  print("args:{}".format(args))
  args = json.loads(args)
  func_call(*list(args.values()))