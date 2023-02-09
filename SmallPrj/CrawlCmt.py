from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import LoginFb

browser  = webdriver.Chrome(executable_path="C:\Program Files\Google\Chrome\Application\chromedriver.exe")

#use function login from LoginFb.py
LoginFb.login(browser)


# browser.get("https://www.facebook.com/fbbongda24h/posts/pfbid09NJ4C6KjAD9NeMMNR3yVFTkjoABtnnWkeKnHw9bpLt2Ch4HDhUx78QZdisF65bkal?__cft__[0]=AZW_-X30GSdqrtEbqoqITY3WS9ujWGAkf8Jjdy1pes9VcB5dh3aL4ABIRa3mvb6uCEfeykCu5zHH4C8urynmkLzk9_OW4VtfK6lgW5OqO_Qz_gDHaz_cNj_xEiwscKYZYb4-ZP1dqugNouv-N6_UZRASLBpx0yyznUncop0bIMnR50MyFp5n_yLFxHjcYfGwmeA&__tn__=%2CO%2CP-R")
# sleep(5)

# showCmt = browser.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/form/div[2]/div[2]/div[1]/div/div[3]/span[1]/a")
# showCmt.click()
# sleep(5)

# # loop if xpath of showMoreCmt exist
# # while showMoreCmt:
# #     showMoreCmt.click()
# #     sleep(5)


# #find div elements where "aria-label" has contain the text "Bình luận"
# cmt = browser.find_elements_by_xpath("//div[contains(@aria-label,'Bình luận')]")

# print(cmt)

# sleep(5)

# browser.close()