import time
from database.Database import Database


def days_to_seconds(days):
    return days * 24 * 60 * 60

async def func_pay_sub(database: Database, user_id, count_day):
    if await database.user_exists_subscribe(user_id) == False:
        time_sub = int(time.time()) + days_to_seconds(count_day)
        await database.add_subscribe(user_id, time_sub)
    else:
        if await database.get_sub_status(user_id) == True:
            time_sub_db = await database.get_timesub_subscribe(user_id)
            time_sub = ((time_sub_db - time.time()) + days_to_seconds(count_day)) + time.time()
            await database.update_timesub_subscribe(user_id, time_sub)
        else:
            time_sub = int(time.time()) + days_to_seconds(count_day)
            await database.update_timesub_subscribe(user_id, time_sub)