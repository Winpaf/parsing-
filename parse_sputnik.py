from bs4 import BeautifulSoup
import sys

def parse_schedule(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    trains = []
    
    table = soup.find('table')
    if not table:
        return trains
    
    rows = table.find_all('tr')[2:]
    seen = set()
    
    for row in rows:
        cells = row.find_all('td')
        
        if len(cells) == 3:
            route_text = cells[0].get_text(' ', strip=True)  # сохраняем пробелы
            time_text = cells[1].get_text(strip=True)
            days_text = cells[2].get_text(strip=True)
            
            # Разделяем тип поезда, маршрут и номер
            route = route_text
            if 'Электричка ' in route_text:
                route = route_text.replace('Электричка ', '')
            elif 'Иволга ' in route_text:
                route = route_text.replace('Иволга ', '')
            elif 'Ласточка ' in route_text:
                route = route_text.replace('Ласточка ', '')
            elif 'Спутник ' in route_text:
                route = route_text.replace('Спутник ', '')
            elif 'Дальний ' in route_text:
                route = route_text.replace('Дальний ', '')
            elif 'Фирменный экспресс ' in route_text:
                route = route_text.replace('Фирменный экспресс ', '')
            
            # Убираем номер поезда из маршрута (последнее слово если это цифры)
            route_parts = route.split(' ')
            if route_parts and route_parts[-1].isdigit():
                route = ' '.join(route_parts[:-1])
            
            # Определяем дни
            day_type = 'ежедневно'
            if 'будн' in days_text.lower():
                day_type = 'будни'
            elif 'выходн' in days_text.lower():
                day_type = 'выходные'
            
            # Убираем дубликаты
            train_id = f"{time_text}-{route}"
            if train_id not in seen and time_text and route:
                seen.add(train_id)
                trains.append({
                    'time': time_text,
                    'route': route,
                    'days': day_type
                })
    
    return trains

def main():
    filter_type = None
    if len(sys.argv) > 1:
        filter_type = sys.argv[1]
    
    try:
        with open('schedule.html', 'r', encoding='utf-8') as f:
            trains = parse_schedule(f.read())
        
        # Фильтрация
        if filter_type in ['будни', 'ежедневно', 'выходные']:
            trains = [t for t in trains if t['days'] == filter_type]
        
        # Вывод
        for train in trains:
            print(f"{train['time']} - {train['route']}")
            
    except FileNotFoundError:
        print("Файл schedule.html не найден")

if __name__ == "__main__":
    main()