# coding:utf8




class HtmlOutputer(object):
    def __init__(self, database_connect):
        self.db = database_connect

    def collect_data(self, data, cid):
        if data:
            cursor = self.db.cursor()
            try:
                # 执行sql语句
                cursor.execute(
                    "INSERT INTO `hstba`.`wp_posts` (`post_author`, `post_date`, `post_date_gmt`, `post_content`, `post_title`, `post_excerpt`,`post_status`, `comment_status`, `ping_status`, `post_modified`, `post_modified_gmt`, `post_parent`, `guid`, `menu_order`, `post_type`, `comment_count`,`to_ping`,`pinged`,`post_content_filtered`) VALUES ('1', NOW(), NOW(), %s, %s,'', 'publish', 'open', 'open', NOW(), NOW(), '0', '', '0', 'post', '0','','','');",
                    (data['main'], data['title'],))
                id = str(int(cursor.lastrowid))
                cursor.execute("update `hstba`.`wp_posts` set `guid` = %s where ID = %s",
                               ('http://www.hstba.com/?p=' + id, id,))
                cursor.execute(
                    "INSERT INTO `hstba`.`wp_term_relationships` (`object_id`, `term_taxonomy_id`, `term_order`) VALUES (%s, %s, '0');",
                    (id, cid,))
                # 提交到数据库执行
                self.db.commit()
                print 'database save %s success' % data['title']
            except:
                # Rollback in case there is any error
                self.db.rollback()

    def is_new_data(self, title):
        title = str(title)
        cursor = self.db.cursor()
        # 执行SQL语句
        cursor.execute("select count(`id`) from `hstba`.`wp_posts` where `post_title`=%s", (title,))
        # 获取所有记录列表
        results = cursor.fetchone()
        if int(results[0]) > 0:
            print 'Data already exists!'
            return True
        return False

    def close_db(self):
        # 关闭数据库连接
        self.db.close()
