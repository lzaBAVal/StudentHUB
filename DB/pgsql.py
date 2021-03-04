import asyncpg, asyncio


class Database:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.pool = loop.run_until_complete(
            asyncpg.create_pool(
                user='samplerole',
                password='Cyberark!123',
                database='testDB',
                host='localhost',
                port='5432'
            )
        )

    @staticmethod
    def formar_args(sql, parameters: dict):
        sql += ' AND '.join([
            f'{item} = ${num}' for num, item in enumerate(parameters, start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, chat_id: int, name: str, surname: str, group_id):
        sql_query = "insert into student (id_chat, u_name, surname, group_id, privilege) values ($1, $2, $3, $4, b\'1\')"
        await self.pool.execute(sql_query, chat_id, name, surname, group_id)

    async def get_user(self, chat_id: int) -> str:
        sql_query = "select * from student where id_chat = $1"
        return await self.pool.fetch(sql_query, chat_id)

    async def check_user(self, chat_id: int) -> str:
        sql_query = "select * from student where id_chat = $1"
        return await self.pool.fetch(sql_query, chat_id)

    async def get_group_sched(self, id_chat: int):
        sql_query = 'select sched_dict from sched_stud where group_id=(select group_id from student where id_chat = $1)'
        return await self.pool.fetchrow(sql_query, id_chat)

    async def get_group_name(self, id_inc: int) -> str:
        sql_query = "select group_name from groups_students where id_inc = $1"
        return await self.pool.fetch(sql_query, id_inc)

    async def get_group_id(self, group_name: str):
        sql_query = "select id_inc from groups_students where group_name = $1"
        return await self.pool.fetchrow(sql_query, group_name)

    async def get_all_groups(self):
        return await self.pool.fetch("select group_name from groups_students")

    async def get_institution(self, id_inc: int):
        sql_query = 'select sched from institution where id_inc = $1'
        return await self.pool.fetch(sql_query, id_inc)

    async def get_institution_url_groups(self, id_inc: int):
        sql_query = 'select url_for_groups from institution where id_inc = $1'
        return await self.pool.fetch(sql_query, id_inc)

    async def get_groups_values(self, institution_id: int):
        sql_query = 'select group_url_value, id_inc from groups_students where institution_id = $1'
        return await self.pool.fetch(sql_query, institution_id)

    async def get_institution_ids(self):
        return await self.pool.fetch('select id_inc from institution')

    async def update_privilege(self, privilege: int, chat_id: int) -> str:
        sql_query = "update student set privilege = b\'$1\' where id_chat = $2"
        return await self.pool.execute(sql_query, privilege, chat_id)

    async def insert_schedule(self, group_id, sched_dict):
        sql_query = "insert into sched_stud(group_id, sched_dict) values ($1, $2);"
        return await self.pool.execute(sql_query, group_id, sched_dict)

    async def insert_group(self, group_name: str, id: int, url_value: str):
        sql_query = 'insert into groups_students(group_name, institution_id, group_url_value) values ($1, $2, $3);'
        return await self.pool.execute(sql_query, group_name, id, url_value)

    async def insert_institution(self, instit_name: str, url: str, url_for_groups: str):
        sql_query = 'insert into institution(instit_name, sched, url_for_groups) values ($1, $2, $3)'
        return await self.pool.execute(sql_query, instit_name, url, url_for_groups)

    async def test_connect(self):
        return await self.pool.execute('select version();')

'''

import psycopg2
from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()

'''