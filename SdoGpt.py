import requests
import json
from bs4 import BeautifulSoup

gpt_url_POST = "https://vip.easychat.work/api/openai/v1/chat/completions" #https://beta.servergpts.com:2053/v1/chat/completions   https://vip.easychat.work/api/openai/v1/chat/completions
sdo_url_GET = "https://sdo24.1580.ru/mod/quiz/attempt.php?attempt=78155&cmid=5303&mdlscrollto=728"
q_number = "q81804"
cmid = "5303"
attempt="78155"
sesskey="cOevSBvprj"
cookie="_ym_uid=1734441442487198253; _ym_d=1734441442; MoodleSession=hfkunejgiilasc8e0ec7cl18ad; MOODLEID1_=sodium%3AGlOZOc232xTL0PNOqi02jBsrJcr2TJsBSn0U1Uf4DjXAG7tzTIPIA9WdHnfP33RdSfI%3D"

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

def sdo_reqest_post(number, answer="oxnacks hack", q_number=q_number, cmid=cmid, attempt=attempt, sesskey=sesskey, fack_number=0):
    url = f"https://sdo24.1580.ru/mod/quiz/processattempt.php?cmid={cmid}&{q_number}:{str(number)}_:flagged=0&{q_number}:{str(number)}_:sequencecheck={fack_number}&{q_number}:{str(number)}_answer={answer}&{q_number}:{str(number)}_-submit=1&attempt={attempt}&thispage={str(int(number)-1)}&nextpage={str(number)}&timeup=0&sesskey={sesskey}&mdlscrollto=360&slots={str(number)}"

    headers = {
        "Content-Type": "application/json",
        "Cookie": cookie
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        return str(response) 
    else:
        print(f"Ошибка SDO: {response.status_code}" )
        return None
    

#####################################################################################################################################333

def parse_problem_statement(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    content_div = soup.find('div', class_='content')
    
    if content_div:
        problem_text = []
        for element in content_div.find_all(['p', 'div']):
            if element.name == 'p':
                problem_text.append(element.get_text(strip=True))
            elif element.name == 'div':
                problem_text.append(element.get_text(strip=True, separator='\n'))
        
        problem_statement = '\n'.join(problem_text)
        
        return problem_statement
    else:
        return "Условие задачи не найдено."

# Пример использования функции
if __name__ == "__main__":
    message = "привет какая ты версия чата gpt "
    # Отправка запроса
    response = gpt_reqest(message)

    # Вывод ответа
    if response:
        print(response)
        #print(json.dumps(response, indent=2))