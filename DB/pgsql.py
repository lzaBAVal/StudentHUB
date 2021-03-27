import asyncpg, asyncio

from logs.logging_core import init_logger, log_encode

logger = init_logger()

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

    #########################
    #        CHECK          #
    #########################

    async def check_user(self, id_chat: int) -> str:
        sql_query = "select * from student where id_chat = $1"
        logger.info('User - {0} check_user'.format(id_chat))
        return await self.pool.fetch(sql_query, id_chat)

    async def check_tester(self, id_chat: int):
        sql_query = "select * from keys where id_chat = $1"
        logger.info('User - {0} check_tester'.format(id_chat))
        return await self.pool.fetch(sql_query, id_chat)

    #########################
    #          GET          #
    #########################

    async def get_user(self, id_chat: int) -> str:
        sql_query = "select * from student where id_chat = $1"
        logger.info('User - {0} get_user'.format(id_chat))
        return await self.pool.fetch(sql_query, id_chat)

    async def get_arh_sched(self, id_chat: int):
        sql_query = 'select sched_arhit from groups_students where id_inc=cast((select group_id from student where ' \
                    'id_chat = $1) as INT) '
        logger.info('User - {0} get_arhit_sched'.format(id_chat))
        return await self.pool.fetchrow(sql_query, id_chat)

    async def get_group_sched(self, id_chat: int):
        sql_query = 'select sched_group from groups_students where id_inc=cast((select group_id from student where ' \
                    'id_chat = $1) as INT) '
        logger.info('User - {0} get_group_sched'.format(id_chat))
        return await self.pool.fetchrow(sql_query, id_chat)

    async def get_group_name(self, id_inc: int) -> str:
        sql_query = "select group_name from groups_students where id_inc = $1"
        return await self.pool.fetch(sql_query, id_inc)

    async def get_group_id(self, group_name: str):
        sql_query = "select id_inc from groups_students where group_name = $1"
        return await self.pool.fetchrow(sql_query, group_name)

    async def get_institution(self, id_inc: int):
        sql_query = 'select url from institution where id_inc = $1'
        return await self.pool.fetch(sql_query, id_inc)

    async def get_institution_url_groups(self, id_inc: int):
        sql_query = 'select url_for_groups from institution where id_inc = $1'
        return await self.pool.fetch(sql_query, id_inc)

    async def get_groups_values(self, institution_id: int):
        sql_query = 'select group_url_value, id_inc from groups_students where institution_id = $1'
        return await self.pool.fetch(sql_query, institution_id)

    async def get_all_groups(self):
        sql_query = 'select group_name from groups_students'
        return await self.pool.fetch(sql_query)

    async def get_groups_name(self):
        sql_query = 'select group_name from groups_students'
        return await self.pool.fetch(sql_query)

    async def get_groups_sched_name_arhit(self, id_inc: int):
        sql_query = 'select group_name, sched_arhit from groups_students where id_inc = $1'
        return await self.pool.fetch(sql_query, id_inc)

    async def get_groups_sched_name_group(self, id_inc: int):
        sql_query = 'select group_name, sched_group from groups_students where id_inc = $1'
        return await self.pool.fetch(sql_query, id_inc)

    async def get_institution_ids(self):
        return await self.pool.fetch('select id_inc from institution')

    async def get_free_hashes(self):
        return await self.pool.fetch('select key_md5 from keys where id_chat = None')

    #########################
    #          ADD          #
    #########################

    async def add_user(self, id_chat: int, name: str, surname: str, group_id):
        sql_query = "insert into student (id_chat, u_name, surname, group_id, privilege) values ($1, $2, $3, $4, " \
                    "b\'1\') "
        logger.info('User - {0} add_user'.format(id_chat))
        await self.pool.execute(sql_query, id_chat, name, surname, group_id)

    async def add_group(self, group_name: str, id_group: int, url_value: str):
        sql_query = 'insert into groups_students(group_name, institution_id, group_url_value) values ($1, $2, $3);'
        return await self.pool.execute(sql_query, group_name, id_group, url_value)

    async def add_institution(self, instit_name: str, url: str, url_for_groups: str):
        sql_query = 'insert into institution(instit_name, sched, url_for_groups) values ($1, $2, $3)'
        return await self.pool.execute(sql_query, instit_name, url, url_for_groups)

    async def add_key(self, hash: str):
        sql_query = 'insert into keys(key_md5) values ($1)'
        return await self.pool.execute(sql_query, hash)

    #########################
    #        UPDATE         #
    #########################

    async def update_arhit_sched(self, sched: str, id_inc: int):
        sql_query = 'update groups_students set sched_arhit = $1 where id_inc = $2;'
        return await self.pool.execute(sql_query, sched, id_inc)

    async def update_group_sched(self, sched: str, id_inc: int):
        sql_query = 'update groups_students set sched_group = $1 where id_inc=cast((select group_id from student ' \
                    'where id_chat = $2) as INT) '

        return await self.pool.execute(sql_query, sched, id_inc)

    async def update_tester(self, id_chat: str, hash: str):
        sql_query = 'update keys set id_chat = $1 where key_md5 = $2;'
        logger.info('User - {0} update_tester'.format(id_chat))
        return await self.pool.execute(sql_query, id_chat, hash)

    async def update_privilege(self, privilege: int, id_chat: int) -> str:
        sql_query = "update student set privilege = b\'$1\' where id_chat = $2"
        logger.info('User - {0} update_privilege, privilege - {1}'.format(id_chat, privilege))
        return await self.pool.execute(sql_query, privilege, id_chat)

    #########################
    #          DEL          #
    #########################

    async def delete_account(self, id_chat: str):
        sql_query = 'delete from student where  id_chat = $1;'
        logger.info('User - {0} delete_account'.format(id_chat))
        return await self.pool.execute(sql_query, id_chat)

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
