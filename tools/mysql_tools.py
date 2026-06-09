# 数据库工具
# 1. list_sql_tables: 列出数据库中所有可用的表，这是了解数据库结构的第一步。
# 2. get_table_data: 读取指定表的前100行数据，用于快速预览数据内容。
# 3. execute_sql_query: 执行自定义SQL查询。当需要复杂的筛选、联接或聚合时使用此工具。
import os

from dotenv import load_dotenv
from mysql.connector import connect, Error

load_dotenv()

# 产生用于连接数据的配置的函数
def get_db_config():
    config = {
        "host": os.getenv("MYSQL_HOST", "localhost"),  # 主机号
        "port": int(os.getenv("MYSQL_PORT", "3306")),  # 端口号
        "user": os.getenv("MYSQL_USER"),  # 用户名
        "password": os.getenv("MYSQL_PASSWORD"),  # 密码
        "database": os.getenv("MYSQL_DATABASE"),  # 数据库名
        "charset": os.getenv("MYSQL_CHARSET", "utf8mb4"),  # 字符集
        "autocommit": True,  # 自动提交事务
    }
    # 过滤掉值None的项
    config = {k: v for k,v in config.items() if v is not None}
    # 检查是否缺少必要配置项，如果缺少，抛出错误
    required_keys = ["user", "password", "database"]
    missing_keys = [k for k in required_keys if k not in config]
    if missing_keys:
        raise ValueError(f"缺少必要配置项: {','.join(missing_keys)}")
    # 返回配置
    return config

_db_config = get_db_config()

# 1. list_sql_tables: 列出数据库中所有可用的表，这是了解数据库结构的第一步。
def list_sql_tables() -> str:
    """
        列出数据库中所有可用的表
    :return:   有表： 可用的表：a,b,c  没表：没有可用的表
    """
    try:
        # 连接数据库，得到连接对象 conn
        with connect(**get_db_config()) as conn:
            # 通过conn得到能执行sql的游标对象 cursor
            with conn.cursor() as cursor:
                # 通过cursor执行查询SQL
                cursor.execute("show tables;")
                # 通过cursor获取结果
                result = cursor.fetchall()
                # 如果没有表，返回：没有可用的表
                if not result:
                    return "没有可用的表"
                # print(result) # [('drugs',), ('inventory',), ('sales_records',)]
                table_names_str = ','.join([item[0] for item in result])
                return f"可用的表：{table_names_str}"
    except Error as e:
        return f"连接数据库失败：{str(e)}"

# 2. get_table_data: 读取指定表的前100行数据，用于快速预览数据内容。
def get_table_data(table_name: str) -> str:
    """
    获取指定表名的前至多100条数据列表，同时带字段名列表
    :param table_name: 表名
    :return:

     表数据
    id   name    age
    1  二狗子    18
    2  驴蛋蛋    19

    返回的结果数据： "id,name,age\n1,二狗子,1\n2,驴蛋蛋,19"
    """
    try:
        # 连接数据库，得到连接对象 conn
        with connect(**_db_config) as conn:
            # 通过conn得到能执行sql的游标对象 cursor
            with conn.cursor() as cursor:
                # 通过cursor执行查询SQL
                sql = f"select * from {table_name} limit 100;"
                cursor.execute(sql)

                # 得到字段名列表
                column_names_str = ','.join(cursor.column_names)
                # print(column_names_str)

                # 获取结果数据, 并拼接成字符串
                result = cursor.fetchall()
                # 如果没有数据，返回：没有数据
                if not result:
                    return f"查询表{table_name},结果没有数据"

                # print(result)  # [(1, '阿莫西林胶囊', '阿莫仙', '国药准字H20051234', '0.25g*24粒')]
                # map(str, item): 将元组中的所有元素都转换为字符串，生成可迭代对象
                data_str = '\n'.join([','.join(map(str, item)) for item in result])
                # print(data_str)
                # 返回包含字段和数据的组合
                return column_names_str + "\n" + data_str
    except Error as e:
        return f"连接数据库失败：{str(e)}"

# 3. execute_sql_query: 执行自定义SQL查询。当需要复杂的筛选、联接或聚合时使用此工具。
def execute_sql_query(sql: str) -> str:
    """
    根据指定sql执行，返回查询的结果
    :param sql: 由大模型生成的sql
    :return:  字段列表和数据列表的字符串
    """
    try:
        # 连接数据库，得到连接对象 conn
        with connect(**_db_config) as conn:
            # 通过conn得到能执行sql的游标对象 cursor
            with conn.cursor() as cursor:
                # 通过cursor执行查询SQL
                cursor.execute(sql)

                # 得到字段名列表
                column_names_str = ','.join(cursor.column_names)
                # print(column_names_str)

                # 获取结果数据, 并拼接成字符串
                result = cursor.fetchall()
                # 如果没有数据，返回：没有数据
                if not result:
                    return f"执行语句{sql},结果没有数据"

                # print(result)  # [(1, '阿莫西林胶囊', '阿莫仙', '国药准字H20051234', '0.25g*24粒')]
                # map(str, item): 将元组中的所有元素都转换为字符串，生成可迭代对象
                data_str = '\n'.join([','.join(map(str, item)) for item in result])
                # print(data_str)
                # 返回包含字段和数据的组合
                return column_names_str + "\n" + data_str
    except Error as e:
        return f"连接数据库失败：{str(e)}"

if __name__ == '__main__':
    # print(get_db_config())
    # print(list_sql_tables())
    # print(get_table_data("drugs"))
    print(execute_sql_query("select * from drugs limit 10"))