import io
import json
import logging
import os
import pickle
import time
from base64 import b64encode
from queue import Queue
import requests
import pandas as pd
import random
import multiprocessing
import psutil

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from app.allOfApp import FbCrawler, flask_app

from app.allOfApp import db
import datetime
from datetime import timedelta

# thuytt
import utils_thuytt as utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import re

POST_Q = multiprocessing.Queue()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# user = "522165579"  # "chuotbeo1284@gmail.com"#"325153458"
# pw = "matkhau2213"  # "thutrang12aaazzzz"#"thutrang12aaazz"
user = "52216557912"  # "chuotbeo1284@gmail.com"#"325153458"
pw = "matkhau2213"
ACCOUNTS = [{'user': '939821396', 'pw': 'chandoi123'},
            {'user': 'independent587@gmail.com', 'pw': 'fromhelloworldwithcode'}]


class TqdmToLogger(io.StringIO):
    """
        Output stream for TQDM which will output to logger module instead of
        the StdOut.
    """
    logger = None
    level = None
    buf = ''

    def __init__(self, logger, level=None):
        super(TqdmToLogger, self).__init__()
        self.logger = logger
        self.level = level or logging.INFO

    def write(self, buf):
        self.buf = buf.strip('\r\n\t ')

    def flush(self):
        self.logger.log(self.level, self.buf)


logger_main = logging.getLogger(__name__)
file_logger = logging.FileHandler(os.path.join(BASE_DIR, 'FbCrawlerDB/log/private_group_crawler.log'), mode='a', encoding='utf-8')
file_logger.setFormatter(logging.Formatter('[%(asctime)s]:[%(levelname)s]:%(message)s'))
logger_main.setLevel(logging.INFO)
logger_main.addHandler(file_logger)
tqdm_out = TqdmToLogger(logger_main, level=logging.INFO)

logger_gcfu = logging.getLogger("get_comments_from_url")
file_logger_gcfu = logging.FileHandler(os.path.join(BASE_DIR, 'FbCrawlerDB/log/get_comments_from_url.log'), mode='a', encoding='utf-8')
file_logger_gcfu.setFormatter(logging.Formatter('[%(asctime)s]:[%(levelname)s]:%(message)s'))
logger_gcfu.setLevel(logging.INFO)
logger_gcfu.addHandler(file_logger_gcfu)

logger_gcfpi = logging.getLogger("get_comments_from_post_id")
file_logger_gcfpi = logging.FileHandler(os.path.join(BASE_DIR, 'FbCrawlerDB/log/get_comments_from_post_id.log'), mode='a', encoding='utf-8')
file_logger_gcfpi.setFormatter(logging.Formatter('[%(asctime)s]:[%(levelname)s]:%(message)s'))
logger_gcfpi.setLevel(logging.INFO)
logger_gcfpi.addHandler(file_logger_gcfpi)
tqdm_out_gcfpi = TqdmToLogger(logger_gcfpi, level=logging.INFO)

logger_cpg = logging.getLogger("crawl_public_group")
file_logger_cpg = logging.FileHandler(os.path.join(BASE_DIR, 'FbCrawlerDB/log/crawl_public_group.log'), mode='a', encoding='utf-8')
file_logger_cpg.setFormatter(logging.Formatter('[%(asctime)s]:[%(levelname)s]:%(message)s'))
logger_cpg.setLevel(logging.INFO)
logger_cpg.addHandler(file_logger_cpg)
tqdm_out_cpg = TqdmToLogger(logger_cpg, level=logging.INFO)

logger_dpud = logging.getLogger("dump_post_url_to_db")
file_logger_dpud = logging.FileHandler(os.path.join(BASE_DIR, 'FbCrawlerDB/log/dump_post_url_to_db.log'), mode='a', encoding='utf-8')
file_logger_dpud.setFormatter(logging.Formatter('[%(asctime)s]:[%(levelname)s]:%(message)s'))
logger_dpud.setLevel(logging.INFO)
logger_dpud.addHandler(file_logger_dpud)
tqdm_out_dpud = TqdmToLogger(logger_dpud, level=logging.INFO)

logger_gpfd = logging.getLogger("get_post_from_db")
file_logger_gpfd = logging.FileHandler(os.path.join(BASE_DIR, 'FbCrawlerDB/log/get_post_from_db.log'), mode='a', encoding='utf-8')
file_logger_gpfd.setFormatter(logging.Formatter('[%(asctime)s]:[%(levelname)s]:%(message)s'))
logger_gpfd.setLevel(logging.INFO)
logger_gpfd.addHandler(file_logger_gpfd)
tqdm_out_gpfd = TqdmToLogger(logger_gpfd, level=logging.INFO)


def thanhpc_dump_url_to_database(group_id_path, cookie_path, scroll, crawled_group_path=None, waited_time_min=5,
                                    batch_group=10,
                                    logger=logger_dpud, driver_name='chrome'):
    logger.info("\n" + '*' * 100)
    time.sleep(2)
    re_run = 1
    while True:
        group_id_df = pd.read_csv(group_id_path, dtype=str)
        try:
            crawled_id_df = pd.read_csv(crawled_group_path)
        except:
            crawled_id_df = pd.DataFrame(columns=group_id_df.columns)
        group_id_df = group_id_df[~group_id_df['group_id'].isin(crawled_id_df['group_id'].tolist())]
        group_ids = list(map(lambda x: str(x[0]), group_id_df.values.tolist()))
        group_ids = group_id_df.values.tolist()
        random.shuffle(group_ids)

        # --------
        cookies = load_cookies(cookie_path)
        cook_q = Queue()
        cook_flag_check = dict()  # cookie flag checkpoint

        for acc in cookies:
            cook_q.put(acc)
            cook_flag_check[acc] = ('normal', datetime.datetime.now())

        web_driver = None
        batch_group = batch_group
        crawled_group = 1

        try:
            while True:
                for acc in cookies:
                    flag, time_block = cook_flag_check[acc]
                    time_stop = datetime.datetime.now() - time_block
                    if flag == 'block_temp' and time_stop >= timedelta(hours=3):
                        logger.info(f'Set normal {acc}')
                        # update flag
                        cook_flag_check[acc] = ('normal', datetime.datetime.now())
                        cook_q.put(acc)
                        logger.info(f"{cook} is expired blocking. Add to cook_queue")
                    else:
                        continue

                logger.info(f'Web driver {web_driver}')
                for g_pram in group_ids:

                    # switch account when crawled enough groups
                    if crawled_group % batch_group == 0:
                        logger.info('Enough group. Switch account...')
                        web_driver, cook_q, cook_flag_check, cook = login_switch_cookie(cook_q, cookies, web_driver,
                                                                                        logger, driver_name,
                                                                                        cook_flag_check)
                        logger.info(f"Queue: {list(cook_q.queue)} '\n cook_flag_check {cook_flag_check}")
                        crawled_group = 1

                    # block_temp -> switch account
                    if web_driver is None:
                        logger.info(f'Switch account ...')
                        web_driver, cook_q, cook_flag_check, cook = login_switch_cookie(cook_q, cookies, web_driver,
                                                                                        logger, driver_name,
                                                                                        cook_flag_check)
                        logger.info(f"Queue: {list(cook_q.queue)} '\n cook_flag_check {cook_flag_check}")
                    crawled_group += 1
                    # hour_range = [7, 8, 11, 12, 15, 16]
                    hour_range = [7]
                    now = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
                    if now.hour in hour_range and re_run == 1:
                        logger.info('Rerun ...')
                        re_run *= -1
                        break
                    elif now.minute not in hour_range:
                        re_run = 1
                    gid = g_pram[0]
                    is_buy_sell = int(g_pram[1])
                    logger.info(f"Crawling group {gid}")

                    def is_checkpoint_group(driver, gid):
                        link_group = driver.current_url + gid
                        driver.get(link_group)
                        time.sleep(3)
                        try:
                            # checkpoint_text = driver.find_element_by_class_name('f.bj').text
                            checkpoint_text = driver.page_source
                        except Exception as e:
                            logger.error(e)
                            return False
                        if 'Bạn tạm thời bị chặn' in checkpoint_text:
                            return True
                        return False

                    if is_checkpoint_group(web_driver, gid):
                        logger.error(f'{cook} is checkpoint !!!')
                        cook_flag_check[cook] = ('block_temp', datetime.datetime.now())
                        if web_driver is None:
                            pass
                        else:
                            web_driver.quit()
                            web_driver = None
                        continue

                    try:
                        logger.info("Go into group ...")
                        if is_buy_sell == False:
                            domain = 'https://m.facebook.com'
                            end_point = ''
                        else:
                            logger.info(f'{gid} is buy &sell group')
                            domain = 'https://facebook.com'
                            end_point = 'buy_sell_discussion'


                        warning_not_exsit = None
                        flag_of_fanpage = False

                        # =============================================================================================

                        try:
                            web_driver.get(f'{domain}/groups/{gid}/{end_point}')
                            time.sleep(3)

                            logger.info(f'Check {gid} is group or fanpage')
                            warning_not_exsit = web_driver.find_elements_by_class_name('_7nyw')

                            if (len(warning_not_exsit) > 0):
                                logger.info(f' {gid} is not a group. It is a fanpage')
                                flag_of_fanpage = True
                                try:
                                    web_driver.get(f'{domain}/{gid}/{end_point}')
                                except:
                                    pass
                            else:
                                logger.info(f'{gid} is exactly a group')


                        # =============================================================================================

                        except:
                            logger.info("\n=======")
                            web_driver = get_web_driver(headless=False, name=driver_name, logger=logger)
                            time.sleep(2)
                            logger.info('Login ...')
                            login(web_driver, user, pw, save_cookies=False)
                            time.sleep(8)
                            logger.info(f"User: {user}, Password: {pw}")

                            # ===================
                            if (flag_of_fanpage):
                                web_driver.get(f'{domain}/{gid}/')
                            else:
                                web_driver.get(f'{domain}/groups/{gid}/')




                        time.sleep(10)
                        logger.info("Scrolling page ...")
                        batch_scroll = 300
                        scroll_sleep = random.randint(5, 10)

                        post_data = []
                        for count_scroll in tqdm(range(scroll), file=tqdm_out_dpud):
                            try:
                                count_scroll += 1
                                if count_scroll % batch_scroll == 0:
                                    scroll_sleep = scroll_sleep + random.randint(4, 10)
                                web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                                time.sleep(scroll_sleep)
                            except Exception as e:
                                logger.exception(str(e))
                                continue


                        now = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
                        if is_buy_sell == False:
                            if (flag_of_fanpage):
                                posts_html = web_driver.find_elements_by_class_name('_55wo._5rgr._5gh8._3drq.async_like')
                                logger.info(f"Dumping {len(posts_html)} post urls ...")
                                for index in tqdm(range(len(posts_html)), file=tqdm_out):
                                    post_html = posts_html[index]
                                    post_url = post_html.find_element_by_class_name('_52jc._5qc4._78cz._24u0._36xo').find_element_by_tag_name('a').get_attribute('href')
                                    posted_time = post_html.find_element_by_class_name('_52jc._5qc4._78cz._24u0._36xo').find_element_by_tag_name('a').text
                                    logger.info(f'Raw time: {posted_time}')
                                    posted_time = convert_fb_datetime(convert_time(posted_time, now), str(now))
                                    logger.info(f'Converted time {posted_time}')
                                    message = post_html.find_element_by_class_name('_5rgt._5nk5._5msi').text
                                    # if message == '':
                                    #     message = post_html.find_element_by_class_name('_5rgu._7dc9._27x0').text
                                    post_data.append({'message': message, 'url': post_url, 'posted_time': posted_time})

                            else:
                                posts_html = web_driver.find_elements_by_class_name('_55wo._5rgr._5gh8.async_like')
                                logger.info(f"Dumping {len(posts_html)} post urls ...")
                                for index in tqdm(range(len(posts_html)), file=tqdm_out):
                                    post_html = posts_html[index]
                                    post_url = post_html.find_element_by_class_name('_52jc._5qc4._78cz._24u0._36xo').find_element_by_tag_name('a').get_attribute('href')
                                    posted_time = post_html.find_element_by_class_name('_52jc._5qc4._78cz._24u0._36xo').find_element_by_tag_name('a').text
                                    logger.info(f'Raw time: {posted_time}')
                                    posted_time = convert_fb_datetime(convert_time(posted_time, now), str(now))
                                    logger.info(f'Converted time {posted_time}')
                                    message = post_html.find_element_by_class_name('_5rgt._5nk5._5msi').text
                                    # if message == '':
                                    #     message = post_html.find_element_by_class_name('_5rgu._7dc9._27x0').text
                                    try:
                                        post_data.append({'message': message, 'url': post_url, 'posted_time': posted_time})
                                    except Exception as e:
                                        print(e)
                        else:
                            # hover
                            post_urls_html = web_driver.find_elements_by_class_name('oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gmql0nx0.gpro0wi8.b1v8xokw')
                            print('len(post_urls_html)', len(post_urls_html))

                            try:
                                all_post_elements = web_driver.find_elements_by_class_name('rq0escxv.l9j0dhe7.du4w35lb.hybvsw6c.io0zqebd.m5lcvass.fbipl8qg.nwvqtn77.k4urcfbm.ni8dbmo4.stjgntxs.sbcfpzgs')
                                web_driver.execute_script("window.scroll({top: 0, left: 0, });")
                                logger.info(f'len(all_post_elements): {len(all_post_elements)}')
                                for i, post_element in enumerate(all_post_elements):
                                    try:
                                        # message, post_url, posted_time = None, None, None
                                        message = post_element.find_element_by_class_name('d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.b0tq1wua.a8c37x1j.fe6kdd0r.mau55g9w.c8b282yb.keod5gw0.nxhoafnm.aigsh9s9.d9wwppkn.hrzyx87i.jq4qci2q.a3bd9o3v.b1v8xokw.oo9gr5id.hzawbc8m').text

                                        # hover
                                        post_html = post_element.find_element_by_class_name('oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gmql0nx0.gpro0wi8.b1v8xokw')
                                        utils.scroll_shim(web_driver, post_html)
                                        time.sleep(1)
                                        try:
                                            print(post_html.text)
                                            temp = WebDriverWait(web_driver, timeout=5).until(EC.element_to_be_clickable((By.CLASS_NAME,"oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gmql0nx0.gpro0wi8.b1v8xokw")))
                                            hover = ActionChains(web_driver).move_to_element(post_html).perform()
                                            print('hover ...')
                                            time.sleep(1)
                                        except Exception as e:
                                            print(e)

                                        # true url
                                        url_element = post_element.find_element_by_class_name('oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gmql0nx0.gpro0wi8.b1v8xokw')
                                        posted_time = url_element.text
                                        posted_time = convert_fb_datetime(convert_time(posted_time, now), str(now))

                                        url = url_element.get_attribute('href')
                                        post_url = 'https://' + 'm' + url.split('/?')[0].split('https://www')[1]
                                        if '#' in post_url:
                                            continue
                                        else:
                                            print(post_url)
                                            post_data.append({'message': message, 'url': post_url, 'posted_time': posted_time})

                                    except Exception as e:
                                        # logger.error(str(e))
                                        pass
                            except Exception as e:
                                logger.error(str(e))
                                continue
                        logger.info(f"Got {len(post_data)} posts")

                        # Dump to fb_crawler
                        for post in post_data:
                            status = 0
                            url = post['url']
                            message = post['message']

                            if(message == '' or url.find('/photos/') != -1):
                                continue

                            created_at_post = post['posted_time']
                            # api_url = 'http://103.231.189.141:3805/detect_property_by_bert'
                            api_url = 'http://103.183.112.241:3805/detect_property_by_bert'
                            # api_url = 'http://localhost:3805/detect_property_by_bert'
                            try:
                                is_property = requests.post(api_url, json={'text': message, 'fbPostId': ''}).json()
                            except:
                                is_property = {}
                            if is_property.get('is_property') is True:
                                logger.info('Is property')
                                status = 1
                            if (flag_of_fanpage):
                                post_id = url.split('story_fbid=')[-1].split('&id=')[0]
                            else:
                                post_id = url.split('permalink/')[-1].split('/')[0]


                            # ===================================
                            if (flag_of_fanpage == False):
                                tag = 'group'
                                try:
                                    int(post_id)
                                except:
                                    post_id = url.split('posts/')[-1].split('/')[0]
                                    try:
                                        int(post_id)
                                    except:
                                        post_id = None
                            else:
                                tag = 'fanpage'

                            logger.info(f'post_id: {post_id}; message: {message}')

                            FbCrawler.insert({'postId': post_id, 'url': url, 'groupId': str(gid), 'status': status, 'createdAtPost': created_at_post, 'tag': tag})

                            time.sleep(random.randint(2, 5))
                        time.sleep(random.randint(10, 20))

                    except Exception as e:
                        web_driver.quit()
                        logger.exception(str(e))
                now = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
                if now.hour in [22, 23]:
                    time.sleep(6 * 60 * 60)
                web_driver.quit()
                if re_run == -1:
                    break
                elif re_run == 1:
                    continue
            time.sleep(60 * waited_time_min)
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, terminating workers")
            parent = psutil.Process()
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()
            if web_driver is None:
                pass
            else:
                web_driver.quit()
        except Exception as e:
            if web_driver is None:
                pass
            else:
                web_driver.quit()
            logger.exception(str(e))




def load_cookies(path):
    cookies_raw = []
    with open(path) as f:
        for i in f:
            try:
                cookies_raw.append(json.loads(i).get('cookie'))
            except:
                cookies_raw.append(i.strip())
    cookies = [convertToCookie(i) for i in cookies_raw]
    return cookies


def convertToCookie(cookie):
    try:
        new_cookie = ["c_user=", "xs="]
        cookie_arr = cookie.split(";")
        for i in cookie_arr:
            if i.__contains__('c_user='):
                new_cookie[0] = new_cookie[0] + (i.strip() + ";").split("c_user=")[1]
            if i.__contains__('xs='):
                new_cookie[1] = new_cookie[1] + (i.strip() + ";").split("xs=")[1]
                if len(new_cookie[1].split("|")):
                    new_cookie[1] = new_cookie[1].split("|")[0]
                if ";" not in new_cookie[1]:
                    new_cookie[1] = new_cookie[1] + ";"

        conv = new_cookie[0] + " " + new_cookie[1]
        if conv.split(" ")[0] == "c_user=":
            return
        else:
            return conv
    except:
        print("Error Convert Cookie")


def get_web_driver(driver=None, name="chrome", headless=False, proxy=None, logger=logger_main):
    options = Options()
    options.headless = headless
    if driver:
        driver.quit()
    # driver = None
    if logger is None:
        print(f'Getting {name} driver')
    logger.info(f'Getting {name} driver')
    if name == 'firefox':
        profile = webdriver.FirefoxProfile()
        profile.set_preference('webdriver_enable_native_events', False)
        profile.set_preference("permissions.default.image", 2)
        if proxy:
            credentials = None
            params = proxy.split(':')
            if len(params) == 2:
                prx = f'{params[0]}:{params[1]}'
                credentials = None
            else:
                credentials = f'{params[2]}:{params[3]}'
            # webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
            #     "httpProxy": prx,
            #     "ftpProxy": prx,
            #     "sslProxy": prx,
            #
            #     "proxyType": "MANUAL",
            #
            # }
            profile.set_preference('network.proxy.type', 1)
            profile.set_preference('network.proxy.http', params[0])
            profile.set_preference('network.proxy.http_port', int(params[1]))
            profile.set_preference('network.proxy.https', params[0])
            profile.set_preference('network.proxy.https_port', int(params[1]))
            profile.set_preference("network.proxy.ssl", params[0])
            profile.set_preference("network.proxy.ssl_port", int(params[1]))
            profile.set_preference("network.proxy.ftp", params[0])
            profile.set_preference("network.proxy.ftp_port", int(params[1]))
            profile.set_preference("network.proxy.socks", params[0])
            profile.set_preference("network.proxy.socks_port", int(params[1]))
            profile.update_preferences()
            # profile.set_preference('network.proxy.no_proxies_on', 'localhost, 127.0.0.1')
            # profile.set_preference("network.proxy.username", params[2])
            # profile.set_preference("network.proxy.password", params[3])
            if credentials:
                profile.add_extension(os.path.join(BASE_DIR, 'tmp/closeproxy.xpi'))
                credentials = b64encode(credentials.encode('ascii')).decode('utf-8')
                profile.set_preference('extensions.closeproxyauth.authtoken', credentials)
        driver = webdriver.Firefox(executable_path=os.path.join(BASE_DIR, "_params/geckodriver"), options=options,
                                   firefox_profile=profile)
    elif name == 'chrome':
        options = webdriver.ChromeOptions()
        # options.add_argument('--proxy-server=%s' % PROXY)
        options.add_argument("--disable-xss-auditor")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-webgl")
        options.add_argument("--disable-popup-blocking")
        if headless:
            options.add_argument("--headless")

        driver = webdriver.Chrome(executable_path=os.path.join(BASE_DIR, "C:\Program Files\Google\Chrome\Application\chromedriver.exe"), options=options)

    return driver


def login_switch_cookie(cook_q, cookies, web_driver, logger, driver_name, cook_flag_check):
    while True:
        logger.info(f'cook_flag_check: {cook_flag_check}')
        logger.info(f'Remain {cook_q.qsize()} alive acc')
        logger.info(f"Cook_q: {list(cook_q.queue)}")
        try:
            cook = cook_q.get(timeout=2)
            flag, time_block = cook_flag_check[cook]
            if flag == 'normal': #
                pass
            else:
                continue
        except:
            # time.sleep(60*60)
            for acc in cookies:
                flag, time_block = cook_flag_check[acc]
                time_stop = datetime.datetime.now() - time_block
                if flag == 'normal':
                    logger.info(f"Add normal {cook} to cook_queue")
                    cook_q.put(acc)
                elif flag == 'block_temp' and time_stop >= timedelta(hours=3):
                    logger.info(f'Set normal {acc}')
                    # update flag
                    cook_flag_check[acc] = ('normal', datetime.datetime.now())
                    cook_q.put(acc)
                    logger.info(f"{cook} is expired blocking. Add to cook_queue")
                else:
                    continue
            if cook_q.qsize() ==0:
                logger.error('All account are being temporary block access link!!!')
                hour_wait = 3
                logger.info(f'Time stop {datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}')
                logger.info(f'Time rerun {(datetime.datetime.now()+ datetime.timedelta(hours=hour_wait)).strftime("%m/%d/%Y, %H:%M:%S")}')
                for _ in tqdm(range(hour_wait),desc=f"waiting {hour_wait} hours..."):
                    for _ in tqdm(range(60)):
                        time.sleep(60)
                continue
        web_driver = login_using_cookies(web_driver, cook, logger, driver_name, headless=False)
        if web_driver is not None:
            cook_q.put(cook) # add put acc_got to cook_queue
            break
        else:
            cook_flag_check[cook] = ('cookie_died', datetime.datetime.now())
    return web_driver, cook_q, cook_flag_check, cook



def login_using_cookies(web_driver, cookie, logger=logger_main, driver_name='chrome', headless=False):
    logger.info("\n=======")
    if web_driver is None:
        pass
    else:
        web_driver.quit()
    time.sleep(1)
    web_driver = get_web_driver(headless=headless, name=driver_name, logger=logger)
    time.sleep(4)
    web_driver.get('https://mbasic.facebook.com/')
    time.sleep(4)
    script = 'javascript:void(function(){ function setCookie(t) { var list = t.split("; "); console.log(list); for (var i = list.length - 1; i >= 0; i--) { var cname = list[i].split("=")[0]; var cvalue = list[i].split("=")[1]; var d = new Date(); d.setTime(d.getTime() + (7*24*60*60*1000)); var expires = ";domain=.facebook.com;expires="+ d.toUTCString(); document.cookie = cname + "=" + cvalue + "; " + expires; } } function hex2a(hex) { var str = ""; for (var i = 0; i < hex.length; i += 2) { var v = parseInt(hex.substr(i, 2), 16); if (v) str += String.fromCharCode(v); } return str; } setCookie("' + cookie + '"); location.href = "https://mbasic.facebook.com"; })();'
    try:
        web_driver.execute_script(script)
        print('Done script')
        time.sleep(5)
        try:
            web_driver.find_element_by_class_name('bh.bf.bg')
            logger.info(f'Login oke {cookie}')
        except:
            logger.error('Error login')
            web_driver.quit()
            return None

        change_language(web_driver)
        web_driver.get('https://mbasic.facebook.com/')
        time.sleep(5)
    except:
        logger.error('Error login type 2')
        web_driver.quit()
        return None
    return web_driver


def change_language(web_driver):
    web_driver.get('https://mbasic.facebook.com/language/')
    time.sleep(3)
    languages_html = web_driver.find_elements_by_class_name('bb.bm.bu.bv')
    if not languages_html:
        languages_html = web_driver.find_elements_by_class_name('ba.s.bb.bc')
    print(len(languages_html))
    for i in languages_html:
        language_name = i.get_attribute('value')
        if language_name == 'Tiếng Việt':
            actionChains = ActionChains(web_driver)
            actionChains.click(i).perform()
            time.sleep(3)
            print('Changed language')
            return


def convert_fb_datetime(fb_time, anchor_time):
    year_replace = datetime.date.today().year
    anchor_time = datetime.datetime.strptime(anchor_time, '%Y-%m-%d %H:%M:%S.%f')
    if 'tháng' in fb_time and 'lúc' in fb_time:
        fb_time = fb_time.split('·')[0].strip()
        try:
            return datetime.datetime.strptime(fb_time, '%d tháng %m lúc %H:%M').replace(year=year_replace)
        except:
            return datetime.datetime.strptime(fb_time, '%d tháng %m, %Y lúc %H:%M')
    elif 'tháng trước' in fb_time:
        fb_time = int(fb_time.split('tháng trước')[0].strip())
        return (anchor_time - datetime.timedelta(days=fb_time * 30))
    elif 'vào' in fb_time:
        anchor_weekday = anchor_time.weekday()
        try:
            fb_time = int(fb_time.split('vào thứ')[1].strip())
        except:
            day_mapping = {'hai': 0, 'ba': 1, 'tư': 2, 'năm': 3, 'sáu': 4, 'bảy': 5, 'chủ nhật': 6}
            if 'chủ nhật' in fb_time.lower():
                fb_time = 'chủ nhật'
            else:
                fb_time = fb_time.split('vào thứ')[1].strip().lower()
            fb_time = day_mapping[fb_time]
        delta_day = anchor_weekday - fb_time
        if delta_day < 0:
            delta_day = delta_day + 7
        return anchor_time - datetime.timedelta(days=delta_day)
    elif 'tuần trước' in fb_time:
        if 'thứ' in fb_time:
            anchor_weekday = anchor_time.weekday()
            fb_time = fb_time.split('tuần trước')[0].split('thứ')[1].strip().lower()
            day_mapping = {'hai': 0, 'ba': 1, 'tư': 2, 'năm': 3, 'sáu': 4, 'bảy': 5, 'chủ nhật': 6}
            fb_time = day_mapping[fb_time]
            delta_day = anchor_weekday - fb_time
            if delta_day < 0:
                delta_day = delta_day + 7
            return (anchor_time - datetime.timedelta(days=delta_day))
        elif 'chủ nhật' in fb_time.lower():
            anchor_weekday = anchor_time.weekday()
            fb_time = 6
            delta_day = anchor_weekday - fb_time
            if delta_day < 0:
                delta_day = delta_day + 7
            return anchor_time - datetime.timedelta(days=delta_day)
        else:
            fb_time = int(fb_time.split('tuần trước')[0].split('thứ')[1].strip())
            return anchor_time - datetime.timedelta(days=fb_time * 7)
    elif 'năm trước' in fb_time:
        fb_time = int(fb_time.split('năm trước')[0].strip())
        return anchor_time - datetime.timedelta(days=fb_time * 365)
    elif 'hôm qua lúc' in fb_time.lower():
        hour_min = fb_time.lower().split('hôm qua lúc')[1].split('·')[0].split(':')
        return (anchor_time - datetime.timedelta(days=1)).replace(hour=int(hour_min[0]), minute=int(hour_min[1]))
    elif 'vừa xong' in fb_time.lower():
        return anchor_time
    else:
        try:
            return datetime.datetime.strptime(fb_time, '%Y-%m-%d %H:%M:%S.%f')
        except:
            return


def convert_time(time_fb, time_now):
    time_fb = time_fb.lower()
    try:
        if 'phút' in time_fb:
            time_value = int(time_fb.split(' ')[0])
            return str(time_now - datetime.timedelta(minutes=time_value))
        elif 'giờ' in time_fb:
            time_value = int(time_fb.split(' ')[0])
            return str(time_now - datetime.timedelta(hours=time_value))
        elif 'ngày' in time_fb:
            time_value = int(time_fb.split(' ')[0])
            return str(time_now - datetime.timedelta(days=time_value))
        elif 'tuần' in time_fb and 'trước' in time_fb and ('Thứ' not in time_fb or 'thứ' not in time_fb):
            time_value = int(time_fb.split(' ')[0])
            return str(time_now - datetime.timedelta(days=time_value * 7))
        elif ('Thứ' in time_fb or 'thứ' in time_fb) and 'tuần' in time_fb:
            time_value = int(time_fb.split(' ')[1])
            return str(time_now - datetime.timedelta(days=time_value * 7))
        elif 'tháng' in time_fb:
            return time_fb
        else:
            return time_fb
    except Exception as e:
        return time_fb


def login(driver, username, password, save_cookies=False, check_cookies=None):
    def _check_cookies(cookies_name, cookies_dir):
        for file in os.listdir(cookies_dir):
            if file.endswith('.pkl'):
                file_name = file.split('.pkl')[0]
                if file_name == cookies_name:
                    with open(os.path.join(cookies_dir, f"{cookies_name}.pkl"), "rb") as c:
                        _cookies = pickle.load(c)
                    return _cookies
        return None

    def _save_cookies(_driver, cookies_name, cookies_dir):
        with open(os.path.join(cookies_dir, f"{cookies_name}.pkl"), 'wb') as file:
            pickle.dump(_driver.get_cookies(), file)

    driver.get("https://www.facebook.com/")
    time.sleep(4)
    if check_cookies:
        cookies = _check_cookies(username, "../tmp/cookies")
    else:
        cookies = None
    if cookies is None:
        inputEmail = driver.find_element_by_id("email")
        inputEmail.send_keys(username)
        inputPass = driver.find_element_by_id("pass")
        inputPass.send_keys(password)
        inputPass.submit()
        if save_cookies:
            cookies = driver.get_cookies()
            with open(os.path.join(BASE_DIR, f"tmp/cookies/{username}.pkl"), 'wb') as file:
                pickle.dump(cookies, file)
    else:
        for cookie in cookies:
            driver.add_cookie(cookie)
    change_language(driver)
    return


def crawl_bds_post_from_db(cookie_path, waited_time=15, driver_name='chrome', batch_acc=100,
                           logger=logger_gpfd):
    logger.info('\n' + '*' * 100)
    cookies = load_cookies(cookie_path)
    cook_q = Queue()
    cook_flag_check = dict()  # cookie flag checkpoint

    for acc in cookies:
        cook_q.put(acc)
        cook_flag_check[acc] = ('normal', datetime.datetime.now())

    re_run = 1
    web_driver = None
    batch_acc = batch_acc
    crawled_post = 0
    try:
        for acc in cookies:
            flag, time_block = cook_flag_check[acc]
            time_stop = datetime.datetime.now() - time_block
            if flag == 'block_temp' and time_stop >= timedelta(hours=3):
                logger.info(f'Set normal {acc}')
                # update flag
                cook_flag_check[acc] = ('normal', datetime.datetime.now())
                cook_q.put(acc)
            else:
                continue

        flag_block = False
        while True:
            if crawled_post % batch_acc == 0 or flag_block:
                flag_block = False
                web_driver, cook_q, cook_flag_check, cook = login_switch_cookie(cook_q, cookies, web_driver, logger,
                                                                                driver_name, cook_flag_check)
                logger.info(f"First queue: {list(cook_q.queue)} '\n cook_flag_check {cook_flag_check}")
            comments_data = []
            post_q = Queue()
            posts_data = None
            try:
                with flask_app.app_context():
                    posts_data = db.session.query(FbCrawler).filter(FbCrawler.isCrawled == 0).order_by(FbCrawler.createdAt.desc()).all()
            except Exception as e:
                print(e)

            logger.info(f'Got {len(posts_data)} posts')
            try:
                logger.info(f'Last time posts_data: {posts_data[-1].createdAtPost} {posts_data[-1].status}')
            except Exception as e:
                print(e)

            for post in posts_data:
                post_q.put(post, timeout=2)
            while not post_q.empty():
                if flag_block:
                    break
                crawled_post += 1

                # thuytt
                if web_driver is None:
                    logger.info(f'Switch account ...')
                    web_driver, cook_q, cook_flag_check, cook = login_switch_cookie(cook_q, cookies, web_driver, logger,
                                                                                    driver_name, cook_flag_check)
                    logger.info(f"Queue: {list(cook_q.queue)} '\n cook_flag_check {cook_flag_check}")
                # ----
                if crawled_post % batch_acc == 0:
                    logger.info(f'Enough batch acc. Switch account ...')
                    web_driver, cook_q, cook_flag_check, cook = login_switch_cookie(cook_q, cookies, web_driver, logger,
                                                                                    driver_name, cook_flag_check)
                    logger.info(f"Queue: {list(cook_q.queue)} '\n cook_flag_check {cook_flag_check}")
                try:
                    post = post_q.get(timeout=2)
                except:
                    time.sleep(10)
                    break
                try:

                    data_returned = get_comments(web_driver, post.url, post.tag, post.groupId, driver_name=driver_name, logger=logger)
                except Exception as e:  # SQL eof (expired connect DB)
                    print(e)
                    db.session.rollback()
                    logger.error('SQL eof')
                    break
                if data_returned.get('error') == 'Error checkpoint':
                    # switch account when block_temp
                    cook_flag_check[cook] = ('block_temp', datetime.datetime.now())
                    logger.error(f'{cook} is temporary block !!!')
                    if web_driver is None:
                        pass
                    else:
                        web_driver.quit()
                        web_driver = None
                    continue
                elif data_returned.get('error') == 'Error get id':
                    post.isCrawled = 2
                    db.session.commit()
                    continue
                elif data_returned.get('error') == 'Error get post data':
                    post.isCrawled = 3
                    db.session.commit()
                    continue
                elif data_returned.get('error') == 'Unknown':
                    post.isCrawled = 4
                    db.session.commit()
                    continue
                elif data_returned.get('error') == 'Error driver':
                    break
                elif data_returned.get('error') == 'Error proxy':
                    continue
                else:
                    logger.info(f"Dumping to db")
                    try:
                        FbCrawler.update_content_post(db, {'postId': data_returned['id'], 'contentPost': data_returned['message'], 'isCrawled': 1, 'updatedAt': data_returned['crawled_time']})
                        flag_block = data_returned['flag_block']

                        new_profile = data_returned['list_user_reaction']
                        with open("profile.json", "r", encoding="utf-8") as file:
                            data = json.load(file)

                        exist_id = set(item['id'] for item in data)
                        for item in new_profile:
                            if item['id'] not in exist_id:
                                data.append(item)
                                exist_id.add(item['id'])

                        with open("profile.json", "w", encoding='utf-8') as file:
                            json.dump(data, file, ensure_ascii=False)
                    except Exception as e:
                        print(e)

                    # dump_to_db(comments_data, image_dir, logger)
                    post.isCrawled = 1
                logger.info(f"Remaining: {post_q.qsize()}")
                now = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
                # if now.hour in [22, 23] :
                #     time.sleep(8 * 60 * 60)
            if flag_block:
                continue
            time.sleep(waited_time * 60)
            try:
                print('dang commit')
                db.session.commit()
            except Exception as e:
                print(f'error commit: {e}')

        if web_driver is None:
            pass
        else:
            web_driver.quit()
        logger.info("Done!")
        pass
    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating workers")
        parent = psutil.Process()
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
        if web_driver is None:
            pass
        else:
            web_driver.quit()
    except Exception as e:
        if web_driver is None:
            pass
        else:
            web_driver.quit()
        logger.exception(str(e))


def get_comments(driver, url, tag, group_id, driver_name='chrome', logger=logger_main):
    try:
        try:
            driver.get(url)
        except:
            if driver is None:
                logger.error('Error driver')
                return {'data': {}, 'error': 'Error driver'}
            else:
                logger.error('Error driver')
                driver.quit()
                return {'data': {}, 'error': 'Error driver'}

        time.sleep(random.randint(2, 4))
        if is_required_login(driver):
            logger.error('Require login')
            return {'data': {}, 'error': 'Error proxy'}

        def is_checkpoint_group(driver):
            try:
                checkpoint_text = driver.find_element_by_class_name('_6j_c').text
                if checkpoint_text == 'Bạn tạm thời bị chặn':
                    return True
            except:
                pass
            return False

        if is_checkpoint_group(driver):
            logger.error('Error checkpoint')
            return {'data': {}, 'error': 'Error checkpoint'}

        try:
            if (tag == 'fanpage'):
                post_id = url.split('story_fbid=')[-1].split('&id=')[0]
                page_id = url.split('&id=')[-1].split('&')[0]
                pass
            elif (tag == 'group'):
                post_id = url.split('permalink/')[-1].split('/')[0]
                page_id = url.split('groups/')[-1].split('/')[0]




        except Exception as e:
            time.sleep(random.randint(1, 3))
            logger.error(f'Error get id')
            # logger.exception(str(e))
            # logger.info(driver.page_source)
            return {'data': {}, 'url': url, 'error': 'Error get id'}
        try:
            now = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
            try:
                post_message = '\n'.join(
                    driver.find_element_by_class_name('story_body_container').text.strip().split('\n')[2:]).strip()
            except:
                post_message = ''

            # data = {'id': post_id,
            #         'from': {'id': driver.find_element_by_class_name('_67lm._77kc').get_attribute('data-sigil').split('ring')[-1],
            #                  'name': driver.find_element_by_class_name('_4g34._5i2i._52we').find_element_by_tag_name('strong').text.strip()},
            #         'message': post_message,
            #         'created_time': convert_fb_datetime(convert_time(driver.find_element_by_class_name('_52jc._5qc4._78cz._24u0._36xo').text, now), str(now)),
            #         'crawled_time': now}




            from_id = driver.find_element_by_class_name('_67lm._77kc').get_attribute('data-sigil').split('ring')[-1]
            from_name = driver.find_element_by_class_name('_4g34._5i2i._52we').find_element_by_tag_name('strong').text.strip()
            created_time = convert_fb_datetime(convert_time(driver.find_element_by_class_name('_52jc._5qc4._78cz._24u0._36xo').text, now), str(now))

            driver.get(driver.find_element_by_class_name('_45m8').get_attribute('href'))



            # list_user = driver.find_element_by_class_name('darkTouch._1aj5.l')
            # for url_user in list_user:
            #     print("hello")

            url_user_reaction = []

            # # show more ==============================================================================================================
            while True:
                try:
                    show_more = driver.find_element_by_class_name('title.mfsm.fcl')
                    show_more.click()
                    time.sleep(2)
                except:
                    break


            list_html_user = driver.find_elements_by_class_name('_4mn.c')
            print(len(list_html_user))


            for index in tqdm(range(len(list_html_user)), file=tqdm_out):
                html_user = list_html_user[index]
                url_user = html_user.find_element_by_tag_name('a').get_attribute('href')
                # name_fb = html_user.find_element_by_tag_name('strong').text
                url_user_reaction.append(url_user)

            flag_block = False
            user_infos = []
            for url in url_user_reaction:
                education = work = living = contact_info = basic_info = user_id = ''

                driver.get(url)

                page_source = driver.page_source
                under_entityId_string = page_source[page_source.find("entity_id:") + len("entity_id:"):]
                user_id = under_entityId_string[:under_entityId_string.find("}")]


                time.sleep(2)
                try:
                    driver.find_element_by_class_name('_5b6s').click()
                    time.sleep(2)
                except:
                    print("It's a fanpage")
                    continue
                try:
                    if driver.find_element_by_class_name('_8rws._55wr.acr.apm.abb') != None:
                        print("Blocked because spam")
                        flag_block = True
                        break
                except:
                    pass
                name_fb = driver.find_element_by_class_name('_6j_c').text
                try:
                    education = driver.find_element_by_id('education').find_element_by_class_name('_55x2._5ji7').text
                except Exception as e:
                    print(e)

                try:
                    work = driver.find_element_by_id('work').find_element_by_class_name('_55x2._5ji7').text
                except Exception as e:
                    print(e)

                try:
                    living = driver.find_element_by_id('living').find_element_by_class_name('_55x2._5ji7').text
                except Exception as e:
                    print(e)

                try:
                    contact_info = driver.find_element_by_id('contact-info').find_element_by_class_name('_55x2._5ji7').text
                except Exception as e:
                    print(e)

                try:
                    basic_info = driver.find_element_by_id('basic-info').find_element_by_class_name('_55x2._5ji7').text
                except Exception as e:
                    print(e)

                user_infos.append({'name_fb': name_fb, 'id': user_id, 'group_id': group_id, 'url_fb': url, 'education': education, 'work': work, 'living': living, 'contact_info': contact_info, 'basic_info': basic_info})

                pass





            data = {'id': post_id,
                    'from': {'id': from_id, 'name': from_name},
                    'message': post_message,
                    'created_time': created_time,
                    'crawled_time': now,
                    'flag_block': flag_block,
                    'list_user_reaction': user_infos}

            return data

        except Exception as e:
            time.sleep(random.randint(2, 4))
            logger.exception(str(e))
            return {'data': data, 'url': url, 'error': 'Unknown'}
    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating workers")
        parent = psutil.Process()
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
        driver.quit()


def is_required_login(web_driver):
    current_url = web_driver.current_url
    if 'login' not in current_url:
        return False
    else:
        return True
    pass



if __name__ == '__main__':
    # thanhpc_dump_url_to_database("tmp/id_group_and_fanpage.csv", "tmp/cookies_url.txt", 10, 1, 10)
    crawl_bds_post_from_db("tmp/cookies_url.txt")
    pass