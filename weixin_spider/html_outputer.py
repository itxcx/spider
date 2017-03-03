# coding:utf8
import uuid

import MySQLdb
import time
import config


class HtmlOutputer(object):
    def __init__(self):
        self.db = None

    def collect_data(self, data, thumbnail_uuid, cid):
        if data:
            self.db = MySQLdb.connect(host=config.DBHOST, user=config.DBUSER, passwd=config.DBPASS, db=config.DBNAME,
                                      charset="utf8")
            cursor = self.db.cursor()
            try:
                # 执行sql语句
                cursor.execute(
                    "INSERT INTO `wp_posts` (`post_author`, `post_date`, `post_date_gmt`, `post_content`, `post_title`, `post_excerpt`,`post_status`, `comment_status`, `ping_status`, `post_modified`, `post_modified_gmt`, `post_parent`, `guid`, `menu_order`, `post_type`, `comment_count`,`to_ping`,`pinged`,`post_content_filtered`) VALUES ('1', NOW(), NOW(), %s, %s,'', 'publish', 'open', 'open', NOW(), NOW(), '0', '', '0', 'post', '0','','','');",
                    (data['main'], data['title'],))
                pid = str(int(cursor.lastrowid))
                cursor.execute("update `wp_posts` set `guid` = %s where ID = %s",
                               ('http://www.hstba.com/?p=' + pid, pid,))
                self.postmeta(thumbnail_uuid, pid, cursor)

                cursor.execute(
                    "INSERT INTO `wp_term_relationships` (`object_id`, `term_taxonomy_id`, `term_order`) VALUES (%s, %s, '0');",
                    (pid, cid,))
                # 提交到数据库执行
                self.db.commit()
                print 'database save %s success' % data['title']
            except:
                # Rollback in case there is any error
                self.db.rollback()
            finally:
                self.db.close()

    def postmeta(self, thumbnail_uuid, id, cursor):
        if not thumbnail_uuid: return

        file_name = ('https://www.hstba.com/wp-content/uploads/%s/%s/' % (
            time.strftime('%Y', time.localtime(time.time())),
            time.strftime('%m', time.localtime(time.time())),)) + thumbnail_uuid + '.jpeg'
        cursor.execute(
            "INSERT INTO `wp_posts` (`post_author`, `post_date`, `post_date_gmt`, `post_title`, `post_status`, `comment_status`, `ping_status`, `post_name`, `post_modified`, `post_modified_gmt`, `post_parent`, `guid`, `menu_order`, `post_type`, `post_mime_type`, `comment_count`) VALUES ('1', NOW(), NOW(), %s, 'inherit', 'open', 'closed', %s, NOW(), NOW(), %s, %s, '0', 'attachment', 'image/jpeg', '0');",
            (thumbnail_uuid, thumbnail_uuid, id, file_name,))
        t_id = str(int(cursor.lastrowid))
        cursor.execute(
            "INSERT INTO `wp_postmeta` (`post_id`, `meta_key`, `meta_value`) VALUES (%s, '_thumbnail_id', %s);",
            (id, t_id,))
        # ---thumbnail_info
        str1 = time.strftime('%Y', time.localtime(time.time())) + '/' + time.strftime('%m', time.localtime(
            time.time())) + '/' + thumbnail_uuid + '.jpeg'
        str2 = time.strftime('%Y', time.localtime(time.time())) + '/' + time.strftime('%m', time.localtime(
            time.time())) + '/' + thumbnail_uuid + '-150x150.jpeg'
        str3 = time.strftime('%Y', time.localtime(time.time())) + '/' + time.strftime('%m', time.localtime(
            time.time())) + '/' + thumbnail_uuid + '-300x169.jpeg'
        cursor.execute(
            "INSERT INTO `wp_postmeta` (`post_id`, `meta_key`, `meta_value`) VALUES (%s, '_wp_attached_file', %s);",
            (t_id, str1,))

        cursor.execute(
            "INSERT INTO `wp_postmeta` (`post_id`, `meta_key`, `meta_value`) VALUES (%s, '_wp_attachment_metadata', %s);",
            (t_id,
             'a:5:{s:5:"width";i:512;s:6:"height";i:512;s:4:"file";s:21:"' + str1 + '";s:5:"sizes";a:2:{s:9:"thumbnail";a:4:{s:4:"file";s:21:"' + str2 + '.jpeg";s:5:"width";i:150;s:6:"height";i:150;s:9:"mime-type";s:10:"image/jpeg";}s:6:"medium";a:4:{s:4:"file";s:21:"' + str3 + '.jpeg";s:5:"width";i:300;s:6:"height";i:300;s:9:"mime-type";s:10:"image/jpeg";}}s:10:"image_meta";a:12:{s:8:"aperture";s:1:"0";s:6:"credit";s:0:"";s:6:"camera";s:0:"";s:7:"caption";s:0:"";s:17:"created_timestamp";s:1:"0";s:9:"copyright";s:0:"";s:12:"focal_length";s:1:"0";s:3:"iso";s:1:"0";s:13:"shutter_speed";s:1:"0";s:5:"title";s:0:"";s:11:"orientation";s:1:"0";s:8:"keywords";a:0:{}}}',))
        cursor.execute(
            "INSERT INTO `wp_postmeta` (`post_id`, `meta_key`, `meta_value`) VALUES (%s, 'views', '1');",
            (t_id,))

    def is_new_data(self, title):
        self.db = MySQLdb.connect(host=config.DBHOST, user=config.DBUSER, passwd=config.DBPASS, db=config.DBNAME,
                                  charset="utf8")
        title = str(title)
        cursor = self.db.cursor()
        # 执行SQL语句
        cursor.execute("select count(`id`) from `hstba`.`wp_posts` where `post_title`=%s", (title,))
        # 获取所有记录列表
        results = cursor.fetchone()
        results = results[0]
        self.db.close()
        if int(results) > 0:
            print 'Data already exists!'
            return True
        return False
