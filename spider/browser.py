# -*- coding: utf-8 -*-
# @Time    : 2021/7/23 9:30
# @Author  : ShaoJK
# @File    : browser.py.py
# @Remark  :
import time
from io import BytesIO
from typing import List

from PIL.Image import open as imageopen

import numpy as np

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class BrowserDriver(webdriver.Chrome):
    def __init__(self,*args,**kwargs):
        super(BrowserDriver, self).__init__(*args,**kwargs)
        self.waiter = WebDriverWait(self, 10, 0.5)

    def click_by_content(self, keyword, label="*", direct=True):
        if direct:
            self.click_direct(self.get_visibility_element("//%s[text()='%s']"%(label,keyword)))
        else:
            self.click_script(self.get_visibility_element("//%s[text()='%s']"%(label,keyword)))

    def loadPage(self):
        js = "window.scrollTo(0,document.body.scrollHeight)"
        self.execute_script(js)

    def input_value(self, ele: WebElement, value: str, enter=False, verify=True, tab=False):
        """
        输入框输入原子操作，输入后，会等到输入的内容和需要输入的内容一致，才会返回。
        :param ele: input元素
        :param value: 需要输入的内容
        :param enter: 是否输入回车
        :return: None
        """
        # 将元素滚动到可见区域
        self.execute_script("arguments[0].scrollIntoView();", ele)
        # 清除内容
        # ele.clear() # 这句好像没有什么用，在特殊情况下还会导致input失去焦点，所以注释掉了 //邵俊凯 2020/10/30 11:14
        # 循环操作，确保输入成功
        if verify:  # 增加可选的验证功能，因为有些场景下，验证代码会出现问题，故可以设置verify为False来回避
            input_success = False
            for i in range(10):
                ele.send_keys(Keys.CONTROL + 'a')
                if value == "":
                    ele.send_keys(Keys.BACKSPACE)
                ele.send_keys(value)
                time.sleep(0.1)
                # 验证输入后的内容是否与需要输入的一致
                input_value = ele.get_attribute("value").strip()
                if input_value == value:
                    if enter:
                        time.sleep(0.1)
                        ele.send_keys(Keys.ENTER)
                        time.sleep(0.5)
                    if tab:
                        ele.send_keys(Keys.TAB)
                        time.sleep(0.5)
                    input_success = True
                    break
            self.assertTrue(input_success, "Input value error.")
        else:
            ele.send_keys(Keys.CONTROL + 'a')
            if value == "":
                ele.send_keys(Keys.BACKSPACE)
            ele.send_keys(value)
            time.sleep(0.1)
            if enter:
                time.sleep(0.1)
                ele.send_keys(Keys.ENTER)
                time.sleep(0.5)
            if tab:
                ele.send_keys(Keys.TAB)
                time.sleep(0.5)

    def click_direct(self, ele: WebElement):
        """
        元素点击。模拟直接点击方式
        :param ele: 元素
        :param text: 名称显示，主要用于日志记录
        :return: None
        """
        # 将元素滚动到可见区域
        try:
            ele.click()
        except:
            self.execute_script("arguments[0].scrollIntoView();", ele)
            self.execute_script("window.scrollBy(0,-200)")  # 向上滑一点，以防被顶部遮挡
            ele.click()
        time.sleep(0.5)

    def click_script(self, ele: WebElement):
        """
        元素点击。使用js脚本点击
        :param ele: 元素
        :param text: 名称显示，主要用于日志记录
        :return: None
        """
        # 将元素滚动到可见区域
        # JS模拟点击
        try:
            self.execute_script("arguments[0].click();", ele)
        except:
            self.execute_script("arguments[0].scrollIntoView();", ele)  # 如果可见目标则不进行滚动，js滚动有时会使前端样式错乱
            self.execute_script("window.scrollBy(0,-200)")  # 向上滑一点，以防被顶部遮挡
            self.execute_script("arguments[0].click();", ele)
        time.sleep(0.5)

    def get_visibility_element(self, xpath: str, er_msg="", timeout=None) -> WebElement:
        """
        页面上定位元素
        :param xpath: 元素XPATH
        :param er_msg: 定位失败后显示的错误信息
        :param timeout: 默认使用config中的timeout，如有设置值，则使用设置的时间，单位：秒
        :return: None
        """
        if not er_msg:
            er_msg = xpath
        locator = (By.XPATH, xpath)
        if timeout:
            ele = WebDriverWait(self, timeout, 0.5).until(ec.visibility_of_element_located(locator), er_msg)
        else:
            ele = self.waiter.until(ec.visibility_of_element_located(locator), er_msg)
        return ele

    def get_visibility_elements(self, xpath: str, er_msg="", timeout=None) -> List[WebElement]:
        """
        页面上定位元素组
        :param xpath: 元素XPATH
        :param er_msg: 定位失败后显示的错误信息
        :param timeout: 默认使用config中的timeout，如有设置值，则使用设置的时间，单位：秒
        :return: None
        """
        if not er_msg:
            er_msg = xpath
        locator = (By.XPATH, xpath)
        if timeout:
            ele_list = WebDriverWait(self, timeout, 0.5).until(ec.visibility_of_all_elements_located(locator),
                                                                      er_msg)
        else:
            ele_list = self.waiter.until(ec.visibility_of_all_elements_located(locator), er_msg)
        return ele_list

    def get_presence_element(self, xpath: str, er_msg="", timeout=None) -> WebElement:
        """
        页面上定位元素，不管是否可见，只要存在
        :param xpath:
        :param er_msg:
        :param timeout:
        :return:
        """
        if not er_msg:
            er_msg = xpath
        locator = (By.XPATH, xpath)
        if timeout:
            ele = WebDriverWait(self, timeout, 0.5).until(ec.presence_of_element_located(locator), er_msg)
        else:
            ele = self.waiter.until(ec.presence_of_element_located(locator), er_msg)
        return ele

    def get_presence_elements(self, xpath: str, er_msg="", timeout=None) -> List[WebElement]:
        """
        页面上定位元素，不管是否可见，只要存在
        :param xpath:
        :param er_msg:
        :param timeout:
        :return:
        """
        if not er_msg:
            er_msg = xpath
        locator = (By.XPATH, xpath)
        if timeout:
            ele_list = WebDriverWait(self, timeout, 0.5).until(ec.presence_of_all_elements_located(locator), er_msg)
        else:
            ele_list = self.waiter.until(ec.presence_of_all_elements_located(locator), er_msg)
        return ele_list

    def wait_appearance(self, xpath: str, timeout=10):
        """
        等待某个元素出现，等待时长为10秒
        :param xpath: 元素XPATH
        :param timeout: 等待的最大时间
        :return: 出现则返回元素，没有则返回None
        """
        locator = (By.XPATH, xpath)
        waiter = WebDriverWait(self, timeout, 0.5)
        try:
            ele = waiter.until(ec.presence_of_element_located(locator))
            return ele
        except TimeoutException:
            return

    def wait_disappearance(self, xpath: str, timeout=10):
        """
        等待某个元素不可见，默认等待时长10秒
        :param xpath:
        :param timeout:
        :return:
        """
        locator = (By.XPATH, xpath)
        waiter = WebDriverWait(self, timeout, 0.5)
        waiter.until_not(ec.visibility_of_element_located(locator))

    def mouse_over(self, ele: WebElement):
        webdriver.ActionChains(self).move_to_element(ele).perform()
        time.sleep(0.5)

    def switch_window(self, index):
        """跳转到指定下标的标签页，index下标从0开始"""
        self.switch_to.window(self.window_handles[index])
        time.sleep(0.5)

    def save_screenshot(self, name, folder_path=None):
        """"函数会自动添加指定的图片后缀，写名字请不要添加后缀。
        参考命名: sys._getframe().f_code.co_name"""
        if folder_path == None:
            folder_path = self.SAVE_SCREENSHOT_PATH
        self.save_screenshot(folder_path + "//%s.png" % name)

    def save_elementshot(self, ele, name, folder_path=None):
        """保存指定元素的截图"""
        if folder_path == None:
            folder_path = self.DOWNLOADS_PATH
        with open(folder_path + "\\%s.jpg" % name, 'wb') as f:
            f.write(ele.screenshot_as_png)

    def mouse_drag(self, ele: WebElement, x_offset, y_offset):
        """将元素拖拽指定距离"""
        webdriver.ActionChains(self).move_to_element_with_offset(ele, ele.size["width"] / 2,
                                                                        ele.size["height"] / 2).drag_and_drop_by_offset(
            ele, x_offset, y_offset).perform()
        time.sleep(0.5)

    def mouse_drag_to_element(self, source: WebElement, target: WebElement, gui=False, duration=0.5):
        """将元素拖拽至指定元素
            gui为True，则使用pyautogui来拖拽图片，此时duration才有效
        """
        # if gui:
        #     pyautogui.FAILSAFE = False
        #     pyautogui.moveTo(source.location['x'] + 20, source.location['y'] + 125)
        #     pyautogui.dragTo(target.location['x'] + 40, target.location['y'] + 155, duration=duration)
        # else:
        webdriver.ActionChains(self).move_to_element(source).drag_and_drop(source, target).perform()
        time.sleep(0.5)

    def double_click(self, ele: WebElement):
        """双击元素"""
        self.execute_script("arguments[0].scrollIntoView();", ele)
        time.sleep(0.25)
        webdriver.ActionChains(self).double_click(ele).perform()

    def right_click(self, ele: WebElement):
        """右击元素"""
        self.execute_script("arguments[0].scrollIntoView();", ele)
        time.sleep(0.1)
        webdriver.ActionChains(self).context_click(ele).perform()
        time.sleep(0.1)

    def control_click(self, ele: WebElement):
        """Control+左击元素"""
        action = webdriver.ActionChains(self)
        action.key_down(Keys.CONTROL).perform()
        action.click(ele).perform()

    def open_page(self, url):
        """在当前标签页中打开url"""
        self.execute_script("window.open('%s');" % url)

    def open_new_page(self, url):
        """在新标签页中打开url"""
        self.execute_script("window.open('%s');" % url)

    def input(self, ele: WebElement, value="", enter=False):
        """
        简化版输入框输入操作
        :param ele: input元素
        :param value: 需要输入的内容
        :param enter: 是否输入回车
        :return: None
        """
        # 将元素滚动到可见区域
        self.execute_script("arguments[0].scrollIntoView();", ele)
        # 清除内容
        ele.send_keys(Keys.CONTROL + 'a')
        if value == "":
            ele.send_keys(Keys.BACKSPACE)
        else:
            ele.send_keys(value)
        time.sleep(0.1)
        if enter:
            time.sleep(0.1)
            ele.send_keys(Keys.ENTER)
            time.sleep(0.5)

    def close(self):
        """关闭当前页面，自动划入下一个标签页，如果下一个标签也不存在，就划入上一个标签页"""
        current_index = self.window_handles.index(self.current_window_handle)
        if current_index + 1 == len(self.window_handles):
            super().close()
            if current_index - 1 >= 0:
                self.switch_window(current_index - 1)
        else:
            super().close()
            self.switch_window(current_index)

    def screenshot_as_array(self, ele: WebElement) -> np.ndarray:
        """对元素进行截屏返回numpy数组"""
        self.execute_script("arguments[0].scrollIntoView();", ele)
        return np.array(imageopen(BytesIO(ele.screenshot_as_png)))