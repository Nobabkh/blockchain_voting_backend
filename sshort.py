from selenium import webdriver
from PIL import Image
import os
import io
import time
import base64
from dto.BooleanBasedmessage import BooleanBasedmessage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def take_full_page_screenshot(url: str) -> list[str]:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # To run the browser in headless mode
    urlpart = url.split(':')
    murl: str
    if(urlpart[0] == 'http' or urlpart[0] == 'https'):
        murl = url
    else:
        murl = 'https://'+url

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(murl)
    except Exception as e:
        print(e)
        return BooleanBasedmessage(state=False, message='url not found')

    # Get dimensions of the entire page
    

    # Set initial window size
    myheight = 200
    driver.set_window_size(1920, 1080)  # Initial width and height
    time.sleep(1)
    total_width = driver.execute_script("return document.body.scrollWidth")
    total_height = driver.execute_script("return document.documentElement.scrollHeight")

    screenshots = []
    listim = 1
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    heightgon = 0
    screenshots.append(driver.get_screenshot_as_png())
    js_code = """
var htmlElement = document.querySelector('html');
var allElements = htmlElement.getElementsByTagName('*');
for (var i = 0; i < allElements.length; i++) {
    allElements[i].style.position = 'static';
}
"""
    #driver.execute_script(js_code)
    while heightgon < total_height:
        # Scroll down to the bottom.

        heightgon = 200*listim
        # if numofsc > 0:
        
        driver.execute_script("window.scrollTo(0, "+str(200*listim)+");")
        
        if(listim != 1):
            screenshots.append(driver.get_screenshot_as_png())
        # else:
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        listim=listim+1
        # Wait to load the page.
        
        # Calculate new scroll height and compare with last scroll height.
        # new_height = driver.execute_script("return document.body.scrollHeight")

    driver.quit()

    # Save each screenshot to a file and stitch them together horizontally
    stitched_image = Image.new('RGB', (total_width, total_height))
    offset = 0
    count =0
    for img in screenshots:
        image = Image.open(io.BytesIO(img))
        if(count != 0):
            print('image croped image '+str(count))
            print(image.height)
            image = image.crop((0, 880, image.width, image.height))
            print(image.height)
            
        image.save('temp'+str(count)+'.png')
        count = count+1
            
        stitched_image.paste(image, (0, offset))
        offset += image.height

    # Combine the saved images into a single stitched image
    output = io.BytesIO()
# Save the stitched image into the binary stream
    stitched_image.save(output, format='PNG') 
    imagestr = base64.b64encode(output.getbuffer()) 
    stitched_image.save('screenshoot.png')
    return [imagestr]


def take_full_page_screenshot_ao(url: str) -> list[str]:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # To run the browser in headless mode
    urlpart = url.split(':')
    murl: str
    if(urlpart[0] == 'http' or urlpart[0] == 'https'):
        murl = url
    else:
        murl = 'https://'+url

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(murl)
    except Exception as e:
        print(e)
        return BooleanBasedmessage(state=False, message='url not found')

    # Get dimensions of the entire page
    

    # Set initial window size
    myheight = 1080
    driver.set_window_size(1920, 1080)  # Initial width and height
    time.sleep(1)
    total_width = driver.execute_script("return document.body.scrollWidth")
    total_height = driver.execute_script("return document.documentElement.scrollHeight")

    
    last_height = driver.execute_script("return document.body.scrollHeight")
    numofsc = last_height/myheight
    
    listim = 1
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    numofsc = last_height/myheight
    while numofsc >= -1:
        # if numofsc > 0:
        driver.execute_script("window.scrollTo(0, "+str(1080*listim)+");")
        # else:
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        listim=listim+1
        numofsc = numofsc-1
    
    driver.set_window_size(total_width, total_height)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
    #stitched_image = Image.new('RGB', (total_width, total_height))
    stitched_image = Image.open(io.BytesIO(driver.get_screenshot_as_png()))
    #stitched_image.save('temporary.png')
    
        # Wait to load the page.
        
        # Calculate new scroll height and compare with last scroll height.
        # new_height = driver.execute_script("return document.body.scrollHeight")

    driver.quit()

    # Save each screenshot to a file and stitch them together horizontally


    # Combine the saved images into a single stitched image
    output = io.BytesIO()
# Save the stitched image into the binary stream
    stitched_image.save(output, format='PNG') 
    imagestr = base64.b64encode(output.getbuffer()) 
    return [imagestr]







def test_screenshot(url: str):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # To run the browser in headless mode
    urlpart = url.split(':')
    murl: str
    if(urlpart[0] == 'http' or urlpart[0] == 'https'):
        murl = url
    else:
        murl = 'https://'+url

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(murl)
    except Exception as e:
        print(e)
        return BooleanBasedmessage(state=False, message='url not found')
    
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    full_height = driver.execute_script("""
    return Math.max(
        document.body.scrollHeight,
        document.documentElement.scrollHeight,
        document.body.offsetHeight,
        document.documentElement.offsetHeight,
        document.body.clientHeight,
        document.documentElement.clientHeight,
        Array.from(document.body.children).reduce((total, el) => total + el.offsetHeight, 0)
    );
""")
    # Get height of the <html> element
    html_height = driver.execute_script("return document.documentElement.scrollHeight;")

    # Get height of the <body> element
    body_height = driver.execute_script("return document.body.scrollHeight;")


    total_height = driver.execute_script("""
        return Array.from(document.body.children).reduce((total, el) => total + el.offsetHeight, 0);
    """)

    print(f"HTML height: {html_height}, Body height: {body_height}, Total children height: {total_height}, Full height : {full_height}")
    
# test_screenshot('https://www.adroll.com')


