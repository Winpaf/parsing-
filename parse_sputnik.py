from bs4 import BeautifulSoup
import sys

def parse_schedule(h):
    s = BeautifulSoup(h, 'html.parser')
    t = []
    
    tb = s.find('table')
    if not tb:
        return t
    
    r = tb.find_all('tr')[2:]
    seen = set()
    
    for row in r:
        c = row.find_all('td')
        
        if len(c) == 3:
            rt = c[0].get_text(' ', strip=True)
            tt = c[1].get_text(strip=True)
            dt = c[2].get_text(strip=True)
            
            # Разделяем тип поезда, маршрут и номер
            rte = rt
            if 'Электричка ' in rt:
                rte = rt.replace('Электричка ', '')
            elif 'Иволга ' in rt:
                rte = rt.replace('Иволга ', '')
            elif 'Ласточка ' in rt:
                rte = rt.replace('Ласточка ', '')
            elif 'Спутник ' in rt:
                rte = rt.replace('Спутник ', '')
            elif 'Дальний ' in rt:
                rte = rt.replace('Дальний ', '')
            elif 'Фирменный экспресс ' in rt:
                rte = rt.replace('Фирменный экспресс ', '')
            
            # Убираем номер поезда из маршрута (последнее слово если это цифры)
            rp = rte.split(' ')
            if rp and rp[-1].isdigit():
                rte = ' '.join(rp[:-1])
            
            # Определяем дни
            dy = 'ежедневно'
            if 'будн' in dt.lower():
                dy = 'будни'
            elif 'выходн' in dt.lower():
                dy = 'выходные'
            
            # Убираем дубликаты
            tid = f"{tt}-{rte}"
            if tid not in seen and tt and rte:
                seen.add(tid)
                t.append({
                    'time': tt,
                    'route': rte,
                    'days': dy
                })
    
    return t

def main():
    ft = None
    if len(sys.argv) > 1:
        ft = sys.argv[1]
    
    try:
        with open('schedule.html', 'r', encoding='utf-8') as f:
            tr = parse_schedule(f.read())
        
        # Фильтрация
        if ft in ['будни', 'ежедневно', 'выходные']:
            tr = [t for t in tr if t['days'] == ft]
        
        # Вывод
        for train in tr:
            print(f"{train['time']} - {train['route']}")
            
    except FileNotFoundError:
        print("Файл schedule.html не найден")

if __name__ == "__main__":
    main()