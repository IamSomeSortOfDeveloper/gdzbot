from typing import NoReturn, Optional
from sqlalchemy import select, ScalarResult, and_, or_, update, delete
from sqlalchemy.dialects.postgresql import Insert
from database.models import Users, Subscribe
import time

class Database:
    def __init__(self, session):
        self.session = session

    async def user_exists(self, user_id: int) -> bool | None:
        zapros = select(Users).where(Users.user_id == user_id)
        employee = await self.session.execute(zapros)
        list_employee = employee.fetchmany(1)
        return bool(len(list_employee))

    async def add_user(self, 
                         user_id: int,
                         refer_start: str,
                         free_day: int) -> NoReturn:
        values = {
            'user_id': user_id,
            'refer_start': refer_start,
            'free_day': free_day
        }

        zapros = Insert(Users).values(**values)
        await self.session.execute(zapros)
        await self.session.commit()
        

    async def add_dialogs(self, 
                          user_id: int, 
                          dialogs: str):

        zapros = update(Users).where(Users.user_id == user_id).values(dialogs = dialogs)
        await self.session.execute(zapros)
        await self.session.commit() 

    async def get_dialogs(self, user_id: int):
        zapros = select(Users.dialogs).where(Users.user_id == user_id)
        employee = await self.session.execute(zapros)
        otvet_db = employee.fetchone()

        for otvet in otvet_db:
            return otvet
        
    async def get_free_day(self, user_id: int):
        zapros = select(Users.free_day).where(Users.user_id == user_id)
        employee = await self.session.execute(zapros)
        otvet_db = employee.fetchone()

        for otvet in otvet_db:
            return otvet
        
    async def update_free_day(self, 
                          user_id: int, 
                          free_day: int):

        zapros = update(Users).where(Users.user_id == user_id).values(free_day = free_day)
        await self.session.execute(zapros)
        await self.session.commit() 
        
    async def get_zapros_count(self, user_id: int):
        zapros = select(Users.zapros_count).where(Users.user_id == user_id)
        employee = await self.session.execute(zapros)
        otvet_db = employee.fetchone()

        for otvet in otvet_db:
            return otvet
        
    async def update_zapros_count(self, 
                          user_id: int, 
                          zapros_count: int):

        zapros = update(Users).where(Users.user_id == user_id).values(zapros_count = zapros_count)
        await self.session.execute(zapros)
        await self.session.commit() 


    async def update_state_user(self, 
                          user_id: int, 
                          state: str):

        zapros = update(Users).where(Users.user_id == user_id).values(state = state)
        await self.session.execute(zapros)
        await self.session.commit() 

    async def get_state_user(self, user_id: int):
        zapros = select(Users.state).where(Users.user_id == user_id)
        employee = await self.session.execute(zapros)
        otvet_db = employee.fetchone()

        for otvet in otvet_db:
            return otvet
        
    async def get_count_in_state_user(self, state: str):
        zapros = select(Users.user_id).where(Users.state == state)
        employee = await self.session.execute(zapros)
        otvet_db = employee.fetchall()

        return len(otvet_db)

    async def update_review_user(self, 
                          user_id: int, 
                          review: int):

        zapros = update(Users).where(Users.user_id == user_id).values(review = review)
        await self.session.execute(zapros)
        await self.session.commit()

    async def get_review_user(self, user_id: int):
        zapros = select(Users.review).where(Users.user_id == user_id)
        employee = await self.session.execute(zapros)
        otvet_db = employee.fetchone()

        for otvet in otvet_db:
            return otvet


    async def user_exists_subscribe(self, user_id: int) -> bool | None:
        zapros = select(Subscribe).where(Subscribe.user_id == user_id)
        employee = await self.session.execute(zapros)
        list_employee = employee.fetchmany(1)
        return bool(len(list_employee))
    
    async def get_sub_status(self, user_id: int):
        zapros = select(Subscribe.time_sub).where(Subscribe.user_id == user_id)
        employee = await self.session.execute(zapros)
        otvet_db = employee.fetchone()

        for otvet in otvet_db:
            if otvet > int(time.time()):
                return True
            else:
                return False

    async def get_all_subscribe(self):
        zapros = select(Subscribe)
        employee = await self.session.execute(zapros)
        otvet_db = employee.fetchall()

        return len(otvet_db)

    async def add_subscribe(self, 
                         user_id: int,
                         time_sub: int) -> NoReturn:
        values = {
            'user_id': user_id,
            'time_sub': time_sub
        }

        zapros = Insert(Subscribe).values(**values)
        await self.session.execute(zapros)
        await self.session.commit()

    async def update_timesub_subscribe(self, 
                          user_id: int, 
                          time_sub: int):

        zapros = update(Subscribe).where(Subscribe.user_id == user_id).values(time_sub = time_sub)
        await self.session.execute(zapros)
        await self.session.commit() 

    async def get_timesub_subscribe(self, user_id: int):
        zapros = select(Subscribe.time_sub).where(Subscribe.user_id == user_id)
        employee = await self.session.execute(zapros)
        otvet_db = employee.fetchone()

        for otvet in otvet_db:
            return otvet


    async def get_all_user(self):
        zapros = select(Users.user_id)
        employee = await self.session.execute(zapros)
        otvet_db = employee.fetchall()

        return len(otvet_db)
        
    async def update_active_user(self, 
                          user_id: int, 
                          active: int):

        zapros = update(Users).where(Users.user_id == user_id).values(active = active)
        await self.session.execute(zapros)
        await self.session.commit()

    async def get_active_user_count(self, active: int):
        zapros = select(Users).where(Users.active == active)
        employee = await self.session.execute(zapros)
        otvet_db = employee.fetchall()

        return len(otvet_db)
    


    async def update_refer_url_user(self, 
                          user_id: int, 
                          my_refer_url: str):

        zapros = update(Users).where(Users.user_id == user_id).values(my_refer_url = my_refer_url)
        await self.session.execute(zapros)
        await self.session.commit()


    async def get_refer_url_user(self, user_id: int):
        zapros = select(Users.my_refer_url).where(Users.user_id == user_id)
        employee = await self.session.execute(zapros)
        otvet_db = employee.fetchone()

        for otvet in otvet_db:
            return otvet
        
    async def get_refer_start_user(self, user_id: int):
        zapros = select(Users.refer_start).where(Users.user_id == user_id)
        employee = await self.session.execute(zapros)
        otvet_db = employee.fetchone()

        for otvet in otvet_db:
            return otvet
        
    async def get_user_onrefer(self, my_refer_url: str):
        zapros = select(Users.user_id).where(Users.my_refer_url == my_refer_url)
        employee = await self.session.execute(zapros)
        otvet_db = employee.fetchone()

        for otvet in otvet_db:
            return otvet
    
    async def get_refer_start_user_count(self, refer_start: str):
        zapros = select(Users.user_id).where(Users.refer_start == refer_start)
        employee = await self.session.execute(zapros)
        otvet_db = employee.fetchall()

        return len(otvet_db)
    

    # ДЕНЬГИ НА ВЫВОД
    # ------------------------------------------------------------------------------------------------------------------------------
    async def update_sum_vivod_user(self, 
                          user_id: int, 
                          sum_vivod: int):

        zapros = update(Users).where(Users.user_id == user_id).values(sum_vivod = sum_vivod)
        await self.session.execute(zapros)
        await self.session.commit()


    async def get_sum_vivod_user(self, user_id: int):
        zapros = select(Users.sum_vivod).where(Users.user_id == user_id)
        employee = await self.session.execute(zapros)
        otvet_db = employee.fetchone()

        for otvet in otvet_db:
            return otvet
    # ------------------------------------------------------------------------------------------------------------------------------


    # ВСЕГО ДЕНЕГ
    # ------------------------------------------------------------------------------------------------------------------------------
    async def update_sum_itog_user(self, 
                          user_id: int, 
                          sum_itog: int):

        zapros = update(Users).where(Users.user_id == user_id).values(sum_itog = sum_itog)
        await self.session.execute(zapros)
        await self.session.commit()


    async def get_sum_itog_user(self, user_id: int):
        zapros = select(Users.sum_itog).where(Users.user_id == user_id)
        employee = await self.session.execute(zapros)
        otvet_db = employee.fetchone()

        for otvet in otvet_db:
            return otvet
    # ------------------------------------------------------------------------------------------------------------------------------