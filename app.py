from flask import Flask, render_template, request
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd


app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/scrap')
def scrap():
    
    text = dict(request.values)['inp']
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        print(text)
        l='https://www.google.com/search?q='+text
        driver.get(l)
        text = driver.find_element_by_xpath('//*[@id="fprsl"]').text
    except Exception as err:
        # print(err)
        pass
    
    print(text)

    l=['https://www.amazon.in/s?k=','https://www.flipkart.com/search?q=']
    for j in range(len(l)):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver= webdriver.Chrome(options=options)
        print(l[j]+ text)
        driver.get(l[j]+text)

        name=[]
        cost=[]
        img=[]
        plink=[]

        e_name = []
        e_cost=[]
        e_img=[]
        e_plink=[]

        if j==0:
            ma=driver.find_elements(By.CLASS_NAME, 's-card-container')

            if len(ma)>0:
                block=ma[:-10]
                for i in range(len(block)):
                    try:
                        n=block[i].find_element(By.TAG_NAME, 'h2').text
                    except:
                        n='Na'
                    try:
                        c=block[i].find_element(By.CLASS_NAME, 'a-price-whole').text
                    except:
                        c='Na'
                    try:
                        im=block[i].find_element(By.CLASS_NAME,'s-image').get_attribute('src')
                    except:
                        im='Na'
                    try:
                        p=block[i].find_element(By.CLASS_NAME,'a-link-normal').get_attribute('href')
                    except:
                        p='Na'    

                    if text.replace(' ','').lower() in n.replace(' ','').lower():
                        name.append(n)
                        cost.append(c)
                        img.append(im)
                        plink.append(p)
                    else:
                        e_name.append(n)
                        e_cost.append(c)
                        e_img.append(im)
                        e_plink.append(p)       
            else:
                block=driver.find_elements_by_class_name('s-asin')
                for i in range(len(block)):
                    n=block[i].find_element('a-size-medium').text
                    try:
                        c=block[i].find_element('a-price-whole').text
                    except:
                        c='Na'
                    try:
                        im=block[i].find_element('s-image').get_attribute('src')
                    except:
                        im='Na'
                    try:
                        p=block[i].find_element('a-link-normal').get_attribute('href')
                    except:
                        p='Na'

                    if text.replace(' ','').lower() in n.replace(' ','').lower():
                        name.append(n)
                        cost.append(c)
                        img.append(im)
                        plink.append(p)
                    else:
                        e_name.append(n)
                        e_cost.append(c)
                        e_img.append(im)
                        e_plink.append(p)      
            
            if len(name) < 5:
                
                name += e_name[:5]
                cost += e_cost[:5]
                img += e_img[:5]
                plink += e_plink[:5]

            data={'PhoneName':name,
            'Price':cost,
            'image':img,
            'link':plink
            }    

            div = len(name)  
        if j==1:
            k=driver.find_elements(By.CLASS_NAME, '_2kHMtA')
            print('k ->', k)
            if len(k)>0:
                block=k
                for i in range(len(block)):
                    n=block[i].find_element(By.CLASS_NAME, '_4rR01T').text
                    try:
                        c=block[i].find_element(By.CLASS_NAME, '_30jeq3').text
                    except:
                        c='Na'
                    try:
                        im=block[i].find_element(By.CLASS_NAME, '_396cs4').get_attribute('src')
                    except:
                        im='Na'
                    try:
                        p=block[i].find_element(By.CLASS_NAME, '_1fQZEK').get_attribute('href')
                    except:
                        p='Na'
                    
                    if text.replace(' ','').lower() in n.replace(' ','').lower():
                        name.append(n)
                        cost.append(c[1:])
                        img.append(im)
                        plink.append(p)
                    else:
                        e_name.append(n)
                        e_cost.append(c)
                        e_img.append(im)
                        e_plink.append(p)    
            else:
                block=driver.find_elements(By.CLASS_NAME,'_4ddWXP')
                for i in range(len(block)):
                    n=block[i].find_element(By.CLASS_NAME,'s1Q9rs').text
                    try:
                        c=block[i].find_element(By.CLASS_NAME,'_30jeq3').text
                    except:
                        c='Na'
                    try:
                        im=block[i].find_element(By.CLASS_NAME,'_3exPp9').get_attribute('src')
                    except:
                        im='Na'
                    try:
                        p=block[i].find_element(By.CLASS_NAME,'_8VNy32').get_attribute('href')
                    except:
                        p='Na'
                    if text.lower() in n.lower():
                        name.append(n)
                        cost.append(c[1:])
                        img.append(im)
                        plink.append(p)
                    else:
                        e_name.append(n)
                        e_cost.append(c)
                        e_img.append(im)
                        e_plink.append(p)    
            if len(name) < 5:
                name += e_name[:5]
                cost += e_cost[:5]
                img += e_img[:5]
                plink += e_plink[:5]
                
            data['PhoneName']=data['PhoneName']+name
            data['Price']=data['Price']+cost
            data['image']=data['image']+img
            data['link']=data['link']+plink

    df=pd.DataFrame(data)
    df = df.to_json()
    print(df)
    driver.close()
            
    return render_template('index.html', arr = df, div = div)

if __name__ == "__main__":
    app.run()  

