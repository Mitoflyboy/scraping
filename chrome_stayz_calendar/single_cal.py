import pandas as pd
from bs4 import BeautifulSoup



#{"property_id": "9207608", "ext_at": "2018-02-21 23:06:09", "review_value": "4.3", "review_count": "3", "page_nbr": 67, "p_nbr": 3326, "calendar": "


html_string = """
<html>
   <body>
   	<table>
<thead>
   <tr>
      <th scope=\"col\"><span title=\"Monday\">Mo</span></th>
      <th scope=\"col\"><span title=\"Tuesday\">Tu</span></th>
      <th scope=\"col\"><span title=\"Wednesday\">We</span></th>
      <th scope=\"col\"><span title=\"Thursday\">Th</span></th>
      <th scope=\"col\"><span title=\"Friday\">Fr</span></th>
      <th scope=\"col\" class=\"ui-datepicker-week-end\"><span title=\"Saturday\">Sa</span></th>
      <th scope=\"col\" class=\"ui-datepicker-week-end\"><span title=\"Sunday\">Su</span></th>
   </tr>
</thead>
<tbody>
   <tr>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">1</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">2</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">3</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">4</span></td>
   </tr>
   <tr>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">5</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">6</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">7</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">8</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">9</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">10</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">11</span></td>
   </tr>
   <tr>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">12</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">13</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">14</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">15</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">16</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">17</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--available\"><span class=\"ui-state-default\">18</span></td>
   </tr>
   <tr>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--arrival-day\"><span class=\"ui-state-default\">19</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">20</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--departure-day\"><span class=\"ui-state-default\">21</span></td>
      <td class=\" ui-datepicker-days-cell-over c-calendar--available ui-datepicker-current-day ui-datepicker-today\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"1\" data-year=\"2018\"><a class=\"ui-state-default ui-state-highlight ui-state-active ui-state-hover\" href=\"#\">22</a></td>
      <td class=\" c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"1\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">23</a></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">24</span></td>
      <td class=\" ui-datepicker-week-end c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"1\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">25</a></td>
   </tr>
   <tr>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"1\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">26</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"1\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">27</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"1\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">28</a></td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-week-end ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-week-end ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
   </tr>
</tbody>
<thead>
   <tr>
      <th scope=\"col\"><span title=\"Monday\">Mo</span></th>
      <th scope=\"col\"><span title=\"Tuesday\">Tu</span></th>
      <th scope=\"col\"><span title=\"Wednesday\">We</span></th>
      <th scope=\"col\"><span title=\"Thursday\">Th</span></th>
      <th scope=\"col\"><span title=\"Friday\">Fr</span></th>
      <th scope=\"col\" class=\"ui-datepicker-week-end\"><span title=\"Saturday\">Sa</span></th>
      <th scope=\"col\" class=\"ui-datepicker-week-end\"><span title=\"Sunday\">Su</span></th>
   </tr>
</thead>
<tbody>
   <tr>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"2\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">1</a></td>
      <td class=\" c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"2\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">2</a></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">3</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">4</span></td>
   </tr>
   <tr>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">5</span></td>
      <td class=\" c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"2\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">6</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"2\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">7</a></td>
      <td class=\" c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"2\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">8</a></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">9</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">10</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">11</span></td>
   </tr>
   <tr>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">12</span></td>
      <td class=\" c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"2\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">13</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"2\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">14</a></td>
      <td class=\" c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"2\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">15</a></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">16</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">17</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">18</span></td>
   </tr>
   <tr>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">19</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">20</span></td>
      <td class=\" c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"2\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">21</a></td>
      <td class=\" c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"2\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">22</a></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">23</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">24</span></td>
      <td class=\" ui-datepicker-week-end c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"2\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">25</a></td>
   </tr>
   <tr>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"2\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">26</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"2\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">27</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"2\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">28</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"2\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">29</a></td>
      <td class=\" c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"2\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">30</a></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">31</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
   </tr>
</tbody>
<thead>
   <tr>
      <th scope=\"col\"><span title=\"Monday\">Mo</span></th>
      <th scope=\"col\"><span title=\"Tuesday\">Tu</span></th>
      <th scope=\"col\"><span title=\"Wednesday\">We</span></th>
      <th scope=\"col\"><span title=\"Thursday\">Th</span></th>
      <th scope=\"col\"><span title=\"Friday\">Fr</span></th>
      <th scope=\"col\" class=\"ui-datepicker-week-end\"><span title=\"Saturday\">Sa</span></th>
      <th scope=\"col\" class=\"ui-datepicker-week-end\"><span title=\"Sunday\">Su</span></th>
   </tr>
</thead>
<tbody>
   <tr>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-week-end ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">1</span></td>
   </tr>
   <tr>
      <td class=\" c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">2</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">3</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">4</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">5</a></td>
      <td class=\" c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">6</a></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">7</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">8</span></td>
   </tr>
   <tr>
      <td class=\" c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">9</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">10</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">11</a></td>
      <td class=\" c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">12</a></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">13</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">14</span></td>
      <td class=\" ui-datepicker-week-end c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">15</a></td>
   </tr>
   <tr>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">16</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">17</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">18</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">19</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">20</a></td>
      <td class=\" ui-datepicker-week-end c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">21</a></td>
      <td class=\" ui-datepicker-week-end c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">22</a></td>
   </tr>
   <tr>
      <td class=\" c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">23</a></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">24</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">25</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">26</span></td>
      <td class=\" c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">27</a></td>
      <td class=\" ui-datepicker-week-end c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"3\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">28</a></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">29</span></td>
   </tr>
   <tr>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">30</span></td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-week-end ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-week-end ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
   </tr>
</tbody>
<thead>
   <tr>
      <th scope=\"col\"><span title=\"Monday\">Mo</span></th>
      <th scope=\"col\"><span title=\"Tuesday\">Tu</span></th>
      <th scope=\"col\"><span title=\"Wednesday\">We</span></th>
      <th scope=\"col\"><span title=\"Thursday\">Th</span></th>
      <th scope=\"col\"><span title=\"Friday\">Fr</span></th>
      <th scope=\"col\" class=\"ui-datepicker-week-end\"><span title=\"Saturday\">Sa</span></th>
      <th scope=\"col\" class=\"ui-datepicker-week-end\"><span title=\"Sunday\">Su</span></th>
   </tr>
</thead>
<tbody>
   <tr>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">1</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">2</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">3</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">4</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">5</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">6</span></td>
   </tr>
   <tr>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">7</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">8</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">9</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">10</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">11</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">12</span></td>
      <td class=\" ui-datepicker-week-end c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"4\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">13</a></td>
   </tr>
   <tr>
      <td class=\" c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"4\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">14</a></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">15</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">16</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">17</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">18</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">19</span></td>
      <td class=\" ui-datepicker-week-end c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"4\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">20</a></td>
   </tr>
   <tr>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"4\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">21</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"4\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">22</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"4\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">23</a></td>
      <td class=\" c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"4\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">24</a></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">25</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">26</span></td>
      <td class=\" ui-datepicker-week-end c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"4\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">27</a></td>
   </tr>
   <tr>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"4\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">28</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"4\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">29</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"4\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">30</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"4\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">31</a></td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-week-end ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-week-end ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
   </tr>
</tbody>
<thead>
   <tr>
      <th scope=\"col\"><span title=\"Monday\">Mo</span></th>
      <th scope=\"col\"><span title=\"Tuesday\">Tu</span></th>
      <th scope=\"col\"><span title=\"Wednesday\">We</span></th>
      <th scope=\"col\"><span title=\"Thursday\">Th</span></th>
      <th scope=\"col\"><span title=\"Friday\">Fr</span></th>
      <th scope=\"col\" class=\"ui-datepicker-week-end\"><span title=\"Saturday\">Sa</span></th>
      <th scope=\"col\" class=\"ui-datepicker-week-end\"><span title=\"Sunday\">Su</span></th>
   </tr>
</thead>
<tbody>
   <tr>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">1</a></td>
      <td class=\" ui-datepicker-week-end c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">2</a></td>
      <td class=\" ui-datepicker-week-end c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">3</a></td>
   </tr>
   <tr>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">4</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">5</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">6</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">7</a></td>
      <td class=\" c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">8</a></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">9</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">10</span></td>
   </tr>
   <tr>
      <td class=\" c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">11</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">12</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">13</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">14</a></td>
      <td class=\" c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">15</a></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">16</span></td>
      <td class=\" ui-datepicker-week-end c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">17</a></td>
   </tr>
   <tr>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">18</a></td>
      <td class=\" c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">19</a></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">20</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">21</span></td>
      <td class=\" c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">22</a></td>
      <td class=\" ui-datepicker-week-end c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">23</a></td>
      <td class=\" ui-datepicker-week-end c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">24</a></td>
   </tr>
   <tr>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">25</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">26</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">27</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">28</a></td>
      <td class=\" c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"5\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">29</a></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">30</span></td>
      <td class=\" ui-datepicker-week-end ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
   </tr>
</tbody>
<thead>
   <tr>
      <th scope=\"col\"><span title=\"Monday\">Mo</span></th>
      <th scope=\"col\"><span title=\"Tuesday\">Tu</span></th>
      <th scope=\"col\"><span title=\"Wednesday\">We</span></th>
      <th scope=\"col\"><span title=\"Thursday\">Th</span></th>
      <th scope=\"col\"><span title=\"Friday\">Fr</span></th>
      <th scope=\"col\" class=\"ui-datepicker-week-end\"><span title=\"Saturday\">Sa</span></th>
      <th scope=\"col\" class=\"ui-datepicker-week-end\"><span title=\"Sunday\">Su</span></th>
   </tr>
</thead>
<tbody>
   <tr>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-week-end ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-week-end ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">1</span></td>
   </tr>
   <tr>
      <td class=\" c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">2</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">3</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">4</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">5</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">6</a></td>
      <td class=\" ui-datepicker-week-end c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">7</a></td>
      <td class=\" ui-datepicker-week-end c-calendar--arrival-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">8</a></td>
   </tr>
   <tr>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">9</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">10</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">11</span></td>
      <td class=\" ui-datepicker-unselectable ui-state-disabled c-calendar--unavailable\"><span class=\"ui-state-default\">12</span></td>
      <td class=\" c-calendar--departure-day\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">13</a></td>
      <td class=\" ui-datepicker-week-end c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">14</a></td>
      <td class=\" ui-datepicker-week-end c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">15</a></td>
   </tr>
   <tr>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">16</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">17</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">18</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">19</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">20</a></td>
      <td class=\" ui-datepicker-week-end c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">21</a></td>
      <td class=\" ui-datepicker-week-end c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">22</a></td>
   </tr>
   <tr>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">23</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">24</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">25</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">26</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">27</a></td>
      <td class=\" ui-datepicker-week-end c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">28</a></td>
      <td class=\" ui-datepicker-week-end c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">29</a></td>
   </tr>
   <tr>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">30</a></td>
      <td class=\" c-calendar--available\" data-handler=\"selectDay\" data-event=\"click\" data-month=\"6\" data-year=\"2018\"><a class=\"ui-state-default\" href=\"#\">31</a></td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-week-end ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
      <td class=\" ui-datepicker-week-end ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled\">&nbsp;</td>
   </tr>
</tbody>
  </table>
   </body>
   </html>
"""

soup = BeautifulSoup(html_string, 'lxml') # Parse the HTML as a string
    
table = soup.find_all('table')[0] # Grab the first table

#new_table = pd.DataFrame(columns=range(0,6), index = [0]) # I know the size 

row_marker = 0
for row in table.find_all('tr'):
    column_marker = 0
    columns = row.find_all('td')
    for column in columns:
        column.get_text()
        print(column.get_text())
        column_marker += 1

#new_table