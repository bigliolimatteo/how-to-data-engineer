import os
from datetime import timedelta, datetime
import uuid
import random
import pandas as pd
import numpy as np

os.makedirs("raw_data/", exist_ok=True)

user_id_population = [str(uuid.uuid4()) for _ in range(1000)]
is_logged_population = [0, 1]
is_logged_probabilities = [0.3, 0.7]
device_type_population = ["android", "iphone", "Iphone", "safari", "chrome", "Google Chrome", "@#$%$^#!^$!#"]
device_type_probabilities = [0.2,  0.1, 0.05, 0.1, 0.2, 0.3, 0.05]
page_type_population = ["HomePage", "Profile", "Notifications", "Messages"]
page_type_probabilities = [0.5, 0.3, 0.1, 0.1]

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def get_env_date(env_var, default, format = "%Y-%m-%d"):
    if "START_DATE" in os.environ:
        return datetime.strptime(os.environ(env_var), format).date()
    return datetime.strptime(default, format).date()

start_date = get_env_date("START_DATE", "2023-10-01")
end_date = get_env_date("END_DATE", "2023-12-31")

for date in daterange(start_date, end_date):
    year = date.strftime("%Y")
    month = date.strftime("%m")
    day = date.strftime("%d") if month != "11" else date.strftime("%-d")

    for hour in range(25):

        if date.weekday() == 6 and hour in [23, 24, 1, 2, 3]: continue

        path = f'raw_data/year={year}/month={month}/day={day}/hour={hour}/'
        if os.path.exists(path): continue
    
        for _ in range(4):
            filename = str(uuid.uuid4())
            data = []

            n_users = random.randrange(10, 20)
            for user in range(n_users):
                user_data = [np.random.choice(user_id_population), np.random.choice(is_logged_population, p=is_logged_probabilities), np.random.choice(device_type_population, p=device_type_probabilities)]
                n_page_visits = random.randrange(5, 10)
                data += [user_data + [np.random.choice(page_type_population, p=page_type_probabilities)] for _ in range(n_page_visits)]

            df = pd.DataFrame(data, columns=["user_id", "is_logged", "device_type", "page_type"])
            os.makedirs(path, exist_ok=True)
            df.to_csv(f'{path}/{filename}.csv', index=False)
