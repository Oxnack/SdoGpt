import requests
import json
from bs4 import BeautifulSoup

gpt_url_POST = "https://vip.easychat.work/api/openai/v1/chat/completions" #https://beta.servergpts.com:2053/v1/chat/completions   https://vip.easychat.work/api/openai/v1/chat/completions

q_number = "q81804"
cmid = "5303"
attempt="78155"
sesskey="9MmElbD962"

cookies = {
    "_ym_uid": "1734441442487198253",
    "_ym_d": "1734441442",
    "MoodleSession": "4sbqup19ak6qv9ku69rb7q75sr",
    "MOODLEID1_": "sodium%3AkA4QJ77a0Wuz%2B%2BLqh3DsbjaVDpufKojcfU%2FbV0hKblG5ccLsfi8ipXt8CHtDgtbPnIY%3D"
}

prompt = "Напиши код на python для решения задачи условие которой будет дальше (вместе с условием может быть очень много ненужной информации о кнопках на странице и тому подобном, читай только условие задачи), в ответ пришли чистый python код абсолютно без комментариев и в коде называй переменные просто как a, b, c, d и так далее"


session = requests.Session()



session.cookies.update(cookies)

# response = session.post(url)


def gpt_reqest(message:str ,url=gpt_url_POST, model="gpt-3.5-turbo"):
    data = {
        "model":model,
        "messages":
        [
            {"role":"system","content":""},
            {"role":"assistant","content":"Привет! Я чат-бот с нейросетью ChatGPT, я работаю на модели gpt-4o-mini и вы можете общатся со мной без ограничения запросов и платных подписок. Напишите ваш первый вопрос."},
            {"role":"user","content":message}
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]  
    else:
        print(f"Ошибка: {response.status_code}")
        return None
    

########################################################################################################

def sdo_reqest_post(number, answer="ddfdfdfdf", q_number=q_number, cmid=cmid, attempt=attempt, sesskey=sesskey, fack_number=0):
    url = f"https://sdo24.1580.ru/mod/quiz/processattempt.php?cmid={cmid}&{q_number}:{str(number)}_:flagged=0&{q_number}:{str(number)}_:sequencecheck={fack_number}&{q_number}:{str(number)}_answer={answer}&{q_number}:{str(number)}_-submit=1&attempt={attempt}&thispage={str(int(number)-1)}&nextpage={str(number)}&timeup=0&sesskey={sesskey}&mdlscrollto=619&slots={str(number)}"

    response = session.post(url)

    if response.status_code == 200:
        return str(response.text) 
    else:
        print(f"Ошибка SDO: {response.status_code}" )
        print(response.text)
        return None
    

#####################################################################################################################################333

# def parse_problem_statement(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
    
#     content_div = soup.find('div', class_='content')
    
#     if content_div:
#         problem_text = []
#         for element in content_div.find_all(['p', 'div']):
#             if element.name == 'p':
#                 problem_text.append(element.get_text(strip=True))
#             elif element.name == 'div':
#                 problem_text.append(element.get_text(strip=True, separator='\n'))
        
#         problem_statement = '\n'.join(problem_text)
        
#         return problem_statement
#     else:
#         return "Условие задачи не найдено."

def parse_problem_statement(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    problem_statement = "Error parse"
    
    try:
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text(separator='\n', strip=True)
        
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        
        problem_statement = '\n'.join(lines)
    except:
        print("Err on parse")
    
    return problem_statement


if __name__ == "__main__":
    response = sdo_reqest_post(2, fack_number=7)
    print(response)
    question = parse_problem_statement(response)
    gpt_response = gpt_reqest(prompt + "Само условие: " + question)

    if gpt_response:
        print(gpt_response)
        print(json.dumps(response, indent=2))
        answer = sdo_reqest_post(2, fack_number=7, answer=gpt_response)
