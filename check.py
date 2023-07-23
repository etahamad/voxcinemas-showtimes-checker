import requests
from bs4 import BeautifulSoup
import time

TELEGRAM_API_TOKEN = "YOUR_TELEGRAM_API_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

def check_ticket_availability(movie_url):
    response = requests.get(movie_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        cinema_locations = soup.find_all("h3", class_="highlight")

        for cinema in cinema_locations:
            cinema_name = cinema.text.strip()
            showtimes_list = cinema.find_next("ol", class_="showtimes")

            if showtimes_list:
                showtimes = showtimes_list.find_all("a", class_="action showtime")
                available_times = [showtime.text.strip() for showtime in showtimes]

                print(f"{cinema_name} - Available showtimes for July 26, 2023:")
                if available_times:
                    for time in available_times:
                        print(time)
                    send_telegram_message(f"{cinema_name} - Showtimes found for July 26, 2023.")
                    return True  # Exit the function and break the loop if showtimes are available

            else:
                print(f"{cinema_name} - No showtimes available for July 26, 2023.")
                print()

    return False  # Return False if no showtimes are available


def send_telegram_message(message):
    telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(telegram_api_url, data=payload)
    if response.status_code == 200:
        print("Telegram message sent successfully.")
    else:
        print("Failed to send Telegram message.")


def main():
    movie_url = "https://egy.voxcinemas.com/movies/oppenheimer?d=20230726#showtimes"
    
    while not check_ticket_availability(movie_url):
        print("No showtimes found. Trying again in 60 seconds...")
        time.sleep(60)


if __name__ == "__main__":
    main()
