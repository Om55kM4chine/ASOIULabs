from bs4 import BeautifulSoup as bs
import requests

weatherTypes = {
    0: "Малый дождь с прояснениями",
    1: "Дождь с прояснениями",
    2: "Сильный дождь с прояснениями",
    3: "Малый снег с прояснениями",
    4: "Снег с прояснениями",
    5: "Сильный снег с прояснениями",
    6: lambda: weatherTypes[0],
    7: lambda: weatherTypes[1],
    8: lambda: weatherTypes[2],
    9: lambda: weatherTypes[3],
    10: lambda: weatherTypes[4],
    11: lambda: weatherTypes[5],
    12: "Малый дождь",
    13: "Дождь",
    14: "Сильный дождь",
    15: "Малый снег",
    16: "Снег",
    17: "Сильный снег",
    18: "Дождь со снегом",
    19: "Град",
    20: "Гроза",
    21: "Дождь с грозой",
    22: "Град с грозой",
    23: "Малооблачно",
    24: lambda: weatherTypes[23],
    25: "Облачно",
    26: "Ясно",
    27: lambda: weatherTypes[26]
}

def main():
    url = "https://yandex.ru/pogoda/ru/omsk/month/february"
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    with open("Lab1/output.txt", "w", encoding="utf-8") as file:
        file.write("Дата : Температура : Состояние погоды : Давление : Влажность : Ветер\n")
        for day in soup.find_all("li", class_="AppMonthCalendar_calendar__item__E7b8r"):
            #Дата
            date = day.find("a")
            if date:
                dateLabel = date.get("aria-label")
                if dateLabel and not "февраля" in dateLabel:
                    continue
            
            #Температура
            temp = day.find("span", class_="AppMonthCalendarDayDetailedInfo_details__temperature__mpLcf")
            if temp:
                tempValue = temp.text
            
            #Состояние погоды
            weather = day.find("div", class_="style_weatherIcon__OE4YL AppMonthCalendarDayDetailedInfo_details__icon__G7qYy")
            if weather:
                weatherValue = weather.get("style")
                if weatherValue:
                    weatherValue = weatherTypes[int(weatherValue.split(":")[-1])] # pyright: ignore[reportAttributeAccessIssue]
            
            #Прочие
            details = day.find("ul", class_="AppMonthCalendarDayDetailedInfo_params__7Z8Yt")
            if details:
                detailsList = details.find_all("li")
                if len(detailsList)==3:
                    pressure=detailsList[0].text
                    humidity=detailsList[1].text
                    wind=detailsList[2].text
            file.write(f"{dateLabel} : {tempValue} : {weatherValue} : {pressure} : {humidity} : {wind}\n")
    pass

if __name__ == "__main__":
    main()