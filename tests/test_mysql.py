import sys, os
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

from settings.config import config
from peewee import Model, MySQLDatabase
from custor.logger import logger

mysqldb = MySQLDatabase('',
                        user=config.BACKEND_MYSQL['user'],
                        password=config.BACKEND_MYSQL['password'],
                        host=config.BACKEND_MYSQL['host'],
                        port=config.BACKEND_MYSQL['port'])

def create_table(db_mysql):
    from db.mysql_model.user import User, Profile, Follower, ChatMessage
    from db.mysql_model.post import Post, PostReply, PostCategory, PostTopic, CollectPost
    from db.mysql_model.common import Notification
    from db.mysql_model.blog import BlogPost, BlogPostLabel, BlogPostCategory

    # -------------------- 建表 ---------------
    db_mysql.create_tables([User, ChatMessage, PostCategory, PostTopic, Post, PostReply, CollectPost, Profile, Follower, Notification, BlogPostCategory, BlogPost, BlogPostLabel], safe=True)

def create_test_data(db_mysql):
    from db.mysql_model.user import User, Profile, Follower, ChatMessage
    from db.mysql_model.post import Post, PostReply, PostCategory, PostTopic, CollectPost
    from db.mysql_model.common import Notification
    from db.mysql_model.blog import BlogPost, BlogPostLabel, BlogPostCategory

    logger.debug("DataBase is not exist, so create test data.")


    # -------------------- 测试用户功能 ---------------
    user_admin = User.new(username='admin', email='admin@jmp.com', password='admin')
    user_test = User.new(username='test', email='test@jmp.com', password='test')

    # -------------------- 测试关注功能 ---------------
    Follower.create(user=user_admin, follower=user_test)

    # -------------------- 测试分类功能 --------------
    logger.debug('''
    版块分类
    专业:
        计算机
    学习:
        学习资料、考研资料、家教、竞赛

    生活:
        共享账号、电影资源、常用软件、电脑故障

    爱好:
        摄影、健身

    未分类:
        校园通知、讨论
    ''')

    postcategory0 = PostCategory.create(name='分类', str='live')
    posttopic0 = PostTopic.create(category=postcategory0, name='爱学习', str='live-study')
    posttopic1 = PostTopic.create(category=postcategory0, name='爱生活', str='live-life')
    posttopic2 = PostTopic.create(category=postcategory0, name='爱管“闲事”', str='live-thing')

    posttopic10 = PostTopic.create(name='通知', str='notice')
    posttopic11 = PostTopic.create(name='讨论', str='discussion')

    # ---------------- 测试新文章 --------------
    post = Post.create(
        topic=posttopic0,
        title='test',
        content=tmp_post,
        user=user_admin
    )

    # ---------------- 测试通知 --------------
    Notification.new_post(post)

    # ------------测试新回复--------------
    postreply = PostReply.create(
            post=post,
            user=user_test,
            content='test'
    )
    post.update_latest_reply(postreply)


    # ---------------- 测试Blog --------------
    bpc0 = BlogPostCategory.create(name='Tornado', str='Tornado')
    bp0 = BlogPost.create(title='Tornado', category=bpc0, content='Tornado content')
    BlogPostLabel.add_post_label('python,tornado', bp0)

    # ---------------- 测试chat --------------
    chat_log_0 = ChatMessage.create(sender=user_admin, receiver=user_test, content='self>other')
    chat_log_0 = ChatMessage.create(sender=user_test, receiver=user_admin, content='other>self')



def mysql_db_init(db_mysql, db_name):
    if not mysqldb.execute_sql("select * from information_schema.schemata where schema_name = '{0}';".format(config.BACKEND_MYSQL['database'])).fetchone():
        mysqldb.execute_sql("create database {0} default character set utf8 default collate utf8_general_ci;".format(config.BACKEND_MYSQL['database']))
    else:
        mysqldb.execute_sql("drop database torweb")
        mysqldb.execute_sql("create database {0} default character set utf8 default collate utf8_general_ci;".format(config.BACKEND_MYSQL['database']))
        pass

    create_table(db_mysql)
    # create_test_data(db_mysql)
    logger.debug('load db from {0}.'.format(db_name))
    import os
    os.system('mysql -u{0} -p{1} {2} <'.format(config.BACKEND_MYSQL['user'], config.BACKEND_MYSQL['password'], config.BACKEND_MYSQL['database'])+os.getcwd()+db_name)
    mysqldb.close()

import html
tmp_post = '''
<pre><code>
'''+html.escape('''
test.test
''')+ '''
</code></pre>
'''

if __name__ == '__main__':
    from db.mysql_model import db_mysql
    db_name = '/db/torweb.sql'
    mysql_db_init(db_mysql, db_name)
