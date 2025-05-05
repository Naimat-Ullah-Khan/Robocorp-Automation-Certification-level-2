import os
import time
import zipfile

from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
from RPA.PDF import PDF
from RPA.Tables import Tables


class Tasks:
    def __init__(self):
        self.browser = Selenium()
    def open_browser(self):
        self.browser.open_available_browser("https://robotsparebinindustries.com/",maximized=True)
    def login(self):
        self.browser.input_text("//input[@id='username']", "maria")
        self.browser.input_text("//input[@id='password']", "thoushallnotpass")
        self.browser.click_button("//button[@class='btn btn-primary']")
    def open_robot_order_website(self):
        self.browser.click_link('//a[@href="#/robot-order"]')
        self.browser.click_button('//div[@class="alert-buttons"]/button[@class="btn btn-dark"]')
        # time.sleep(3)

    def get_orders(self):
        http = HTTP()
        csv_path = "output/orders.csv"
        http.download(url="https://robotsparebinindustries.com/orders.csv", target_file=csv_path, overwrite=True)

        tables = Tables()
        orders = tables.read_table_from_csv(csv_path)
        return orders

    def fill_form(self, data):
        self.browser.select_from_list_by_value("//select[@id='head']", str(data["Head"]))
        self.browser.click_button(f"//input[@value={data['Body']}]")
        self.browser.input_text('//input[@min="1"]', data['Legs'])
        self.browser.input_text('//input[@id="address"]', data['Address'])

        while True:
            try:
                self.browser.click_button("//button[@class='btn btn-primary']")
                time.sleep(2)
                screenshots = self.screenshot_capture()

                pdf = PDF()
                pdf.add_files_to_pdf(
                    files=screenshots,
                    target_document="output/robot.pdf",
                    append=True
                )

                self.browser.click_button("//button[@id='order-another']")
                break
            except:
                pass


        self.browser.click_button('//div[@class="alert-buttons"]/button[@class="btn btn-dark"]')

    def order_bots(self):
        orders = self.get_orders()
        for order in orders:
            self.fill_form(order)

    def screenshot_capture(self):
        screenshots_list=[]
        s1 = self.browser.capture_element_screenshot("//div[@id='receipt']", f"output/screenshot1.png")
        s2 = self.browser.capture_element_screenshot("//div[@id='robot-preview-image']", f"output/screenshot2.png")
        screenshots_list.append(s1)
        screenshots_list.append(s2)
        return screenshots_list

    def archive_receipts(self):
        with zipfile.ZipFile("robot.zip", "w") as myzip:
            myzip.write('output/robot.pdf',arcname='robot.pdf')
try:
    os.remove("output/robot.pdf")
except:
    pass
try:
    os.remove("robot.zip")
except:
    pass
p=Tasks()
p.open_browser()
p.login()
p.open_robot_order_website()
p.order_bots()
p.archive_receipts()
time.sleep(10)

