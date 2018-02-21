import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import datetime
import time
import json
import logging
from lxml import etree


calendar_basic = "<thead><tr><th scope=\"col\"><span title=\"Monday\">Mo</span></th><th scope=\"col\"><span title=\"Tuesday\">Tu</span></th><th scope=\"col\"><span title=\"Wednesday\">We</span></th><th scope=\"col\"><span title=\"Thursday\">Th</span></th><th scope=\"col\"><span title=\"Friday\">Fr</span></th><th scope=\"col\" class=\"ui-datepicker-week-end\"><span title=\"Saturday\">Sa</span></th><th scope=\"col\" class=\"ui-datepicker-week-end\"><span title=\"Sunday\">Su</span></th></tr></thead><tbody><tr><td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td><td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td><td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td><td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">1</span></td><td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">2</span></td><td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">3</span></td><td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">4</span></td></tr><tr><td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">5</span></td><td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">6</span></td><td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">7</span></td><td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">8</span></td><td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">9</span></td><td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">10</span></td><td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--arrival-day\"><span class=\"ui-state-default\">11</span></td></tr><tr><td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--departure-day\"><span class=\"ui-state-default\">12</span></td><td class=\" ui-datepicker-days-cell-over c-calendar--available ui-datepicker-current-day ui-datepicker-today\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"1\" data-year=\"2018\"><a class=\"ui-state-default ui-state-highlight ui-state-active ui-state-hover\" href=\"#\">13</a></td><td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"1\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">14</a></td><td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"1\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">15</a></td><td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"1\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">16</a></td><td class=\" ui-datepicker-week-end c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"1\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">17</a></td><td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">18</span></td></tr><tr><td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">19</span></td><td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">20</span></td><td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">21</span></td><td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">22</span></td><td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">23</span></td><td class=\" ui-datepicker-week-end c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"1\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">24</a></td><td class=\" ui-datepicker-week-end c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"1\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">25</a></td></tr><tr><td class=\" c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"1\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">26</a></td><td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">27</span></td><td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">28</span></td><td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td><td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td><td class=\" ui-datepicker-week-end ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td><td class=\" ui-datepicker-week-end ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td></tr></tbody>"


calendar_header = "<html><body><table>"

calendar_footer = "</table></body></html>"

cal_full = calendar_header + calendar_basic + calendar_footer

print(cal_full)

table = etree.HTML(cal_full).find("table")
rows = iter(table)

headers = [col.text for col in next(rows)]
for row in rows:
    values = [col.text for col in row]
    print(dict(zip(headers, values)))