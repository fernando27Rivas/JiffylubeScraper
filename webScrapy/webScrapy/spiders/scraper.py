# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from webScrapy.items import WebscrapyItem
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime,timedelta
from webScrapy import settings
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options


class ScraperSpider(CrawlSpider):
    name = 'scraper'
    allowed_domains = ['grow.jiffylube.com']
    search_url = 'https://grow.jiffylube.com/posreportingservice/default.aspx'
    start_urls = ['https://grow.jiffylube.com/posreportingservice/default.aspx']

    def parse(self, response):
        url = "https://grow.jiffylube.com/posreportingservice/default.aspx"
        user = settings.USER
        passw = settings.PASSW
        choice = settings.SELECT
        choice2 = settings.SELECT2
        
        chrome_options = Options()
        prefs = {"download.default_directory":'/home/avalogics/Downloads/JIFFI'}
        chrome_options.add_experimental_option("prefs", prefs)
        #chrome_options.set_headless(True)
        #chrome_options.add_argument('--disable-extensions')
        #chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)
        #browser = webdriver.Chrome('/usr/bin/chromedriver')
        browser.get(url)
        time.sleep(2)
        
        name_box = browser.find_element_by_id("txtUserName")
        name_box.send_keys(user)
        pass_box = browser.find_element_by_id("txtPassword")
        pass_box.send_keys(passw)
        select_box = Select(browser.find_element_by_id("ddlEntity"))
        select_box.select_by_visible_text(choice)
        browser.find_element_by_id("btnLogin").click()
        time.sleep(2)
        #iframe = browser.find_elements_by_tag_name('iframe')[0]
        browser.switch_to.frame('frmLeftNav')
        #rests = browser.find_elements_by_xpath("/html/body/table/tbody/tr[2]/td[2]/a")
        rests = browser.find_elements_by_class_name("FormElement")
        rests[1].click()
        time.sleep(5)
        browser.switch_to.default_content()
        browser.switch_to.frame('frmBody')
        select2_box = Select(browser.find_element_by_id("lbReports"))
        select2_box.select_by_visible_text(choice2)
        
        from_box = browser.find_element_by_id("dpFromDate_dateTextBox")
        from_box.send_keys((datetime.now()-timedelta(1)).strftime("%m/%d/%Y"))
        to_box = browser.find_element_by_id("dpToDate_dateTextBox")
        to_box.send_keys(time.strftime("%m/%d/%Y"))
        time.sleep(1)
        browser.find_element_by_id("btnExecute").click()
        time.sleep(60)
        
        browser.close()


