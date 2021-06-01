from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

import time

password = "YOUR METAMASK PASSWORD HERE"

#function to intialize the driver with desired settings
def startChrome():
    # setup chrome with default profile
    options = webdriver.ChromeOptions() 
    options.add_argument("user-data-dir=PATH TO YOUR CHROME PROFILE SO YOU DONT NEED SEED PHRASE") #Path to your chrome profile
    options.add_argument("--enable-gpu")
    driver = webdriver.Chrome(chrome_options=options)

    return driver

def setupMetamaskWithSeedPhrase():
    driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")
    time.sleep(1)
    getStarted = driver.find_element_by_class_name("button.btn-primary.first-time-flow__button").click()
    time.sleep(1)
    importWallet = driver.find_element_by_xpath("//*[contains(text(), 'Import wallet')]").click()
    time.sleep(1)
    agree = driver.find_element_by_xpath("//*[contains(text(), 'I Agree')]").click()

#Connects to your metamask wallet and then connects spirit to your metamask
def connectWalletToSpirit():
    #open spirit and save window
    driver.get("https://app.spiritswap.finance/#/farms")
    spiritWindow = driver.window_handles[0]

    #necessary to get metamask window to popup and save metamask window
    driver.get('chrome://extensions/')
    driver.get("https://app.spiritswap.finance/#/farms")
    time.sleep(2.5)

    connectButton = driver.find_element_by_xpath("//*[contains(text(), 'Connect')]")
    connectButton.click()
    time.sleep(2)
    metamaskButton = driver.find_element_by_xpath("//*[contains(text(), 'Metamask')]")
    metamaskButton.click()
    time.sleep(5)
    metamaskWindow = driver.window_handles[1]

    #enter password to metamask
    driver.switch_to_window(metamaskWindow)
    passwordFill = driver.find_element_by_id("password")
    passwordFill.send_keys(password)
    driver.find_element_by_xpath("//*[contains(text(), 'Unlock')]").click()
    
    driver.switch_to_window(spiritWindow)
    #connect metamask to spirit
    # driver.switch_to_window(spiritWindow)
    # connectButton = driver.find_element_by_xpath("//*[contains(text(), 'Connect')]")
    # connectButton.click()
    # time.sleep(2)
    # metamaskButton = driver.find_element_by_xpath("//*[contains(text(), 'Metamask')]")
    # metamaskButton.click()

#Harvests your pools in spirit
def spiritHarvest(numPools):
    time.sleep(10)
    harvests = driver.find_elements_by_xpath("//*[contains(text(), 'Harvest')]")
    for x in range(0,len(harvests)):
        harvests[x].click()
    print(len(harvests))

    time.sleep(5)
    driver.switch_to_window(driver.window_handles[1])
    time.sleep(2)
    gasFee = 0.0 
    harvestGasFees = 0.0
    for i in range(0, numPools):
        time.sleep(2)
        gasFee = driver.find_element_by_class_name("currency-display-component.confirm-detail-row__primary").get_attribute("title")
        harvestGasFees += float(gasFee)
        driver.find_element_by_xpath("//*[contains(text(), 'Confirm')]").click()

    driver.switch_to_window(driver.window_handles[0])
    print("Gas Fees to Harvest: " + str(harvestGasFees) + "FTM")
    return harvestGasFees


def give2percentToGas():
    driver.get("https://swap.spiritswap.finance/#/swap?inputCurrency=0xe9e7cea3dedca5984780bafc599bd69add087d56&outputCurrency=0x5Cc61A78F164885776AA610fb0FE1257df78E59B")
    
    spiritBalance = str(WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Balance')]"))).text)
    numSpiritBalance = spiritBalance.split(' ')
    gasFeeComp = float(numSpiritBalance[1]) * 0.02
    
    driver.find_element_by_class_name("sc-bdfBwQ.hjcEfk").click()

    driver.find_element_by_class_name("sc-aKZfe.fvHEZR.token-amount-input").click()
    driver.find_element_by_class_name("sc-aKZfe.fvHEZR.token-amount-input").send_keys(str(gasFeeComp))

    driver.find_element_by_xpath("//*[contains(text(), 'Select a currency')]").click()
    
    try: 
        driver.find_element_by_xpath("//div[@title='Fantom']").click()
    except NoSuchElementException:
        driver.find_element_by_xpath("//*[contains(text(), 'FTM')]").click()

    WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.ID, "swap-button"))).click()
    driver.find_element_by_id("confirm-swap-or-send").click()
    time.sleep(2)
    driver.switch_to_window(driver.window_handles[1])
    driver.find_element_by_xpath("//*[contains(text(), 'Confirm')]").click()
    driver.switch_to_window(driver.window_handles[0])



def swapHalf(coin):
    driver.get("https://swap.spiritswap.finance/#/swap?inputCurrency=0xe9e7cea3dedca5984780bafc599bd69add087d56&outputCurrency=0x5Cc61A78F164885776AA610fb0FE1257df78E59B")
    
    spiritBalance = str(WebDriverWait(driver, 45).until(ec.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Balance')]"))).text)
    numSpiritBalance = spiritBalance.split(' ')
    halfBalance = float(numSpiritBalance[1]) * 0.5

    if any("SPIRIT" in s for s in coins):
        print("Spirit IS one of the coins")
        driver.find_element_by_class_name("sc-bdfBwQ.hjcEfk").click()
        driver.find_element_by_class_name("sc-aKZfe.fvHEZR.token-amount-input").click()
        driver.find_element_by_class_name("sc-aKZfe.fvHEZR.token-amount-input").send_keys(str(halfBalance))

        spiritIndex = coins.index("SPIRIT")
        if spiritIndex == 0:
            otherCoinIndex = 1
        else:
            otherCoinIndex = 0

        driver.find_element_by_xpath("//*[contains(text(), 'Select a currency')]").click()

        try: 
            driver.find_element_by_xpath("//div[@title='" + coin[otherCoinIndex] + "']").click()
        except NoSuchElementException:
            driver.find_element_by_xpath("//*[contains(text(), '" + coin[otherCoinIndex] + "')]").click()

        WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.ID, "swap-button"))).click()
        driver.find_element_by_id("confirm-swap-or-send").click()
        time.sleep(2)
        driver.switch_to_window(driver.window_handles[1])
        driver.find_element_by_xpath("//*[contains(text(), 'Confirm')]").click()
    
    else:
        print("Spirit IS NOT one of the coins")
        for x in range(0,2):
            if x > 0:
                driver.refresh()

            time.sleep(2)
            driver.find_element_by_class_name("sc-bdfBwQ.hjcEfk").click()
            driver.find_element_by_class_name("sc-aKZfe.fvHEZR.token-amount-input").click()
            driver.find_element_by_class_name("sc-aKZfe.fvHEZR.token-amount-input").send_keys(str(halfBalance))


            driver.find_element_by_xpath("//*[contains(text(), 'Select a currency')]").click()

            try: 
                driver.find_element_by_xpath("//div[@title='" + coin[x] + "']").click()
            except NoSuchElementException:
                driver.find_element_by_xpath("//*[contains(text(), '" + coin[x] + "')]").click()

            WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.ID, "swap-button"))).click()
            driver.find_element_by_id("confirm-swap-or-send").click()
            time.sleep(2)
            driver.switch_to_window(driver.window_handles[1])
            time.sleep(1)
            driver.find_element_by_xpath("//*[contains(text(), 'Confirm')]").click()
            time.sleep(10)
    
    driver.switch_to_window(driver.window_handles[0])


def addLiquidity(coin):
    driver.get("https://swap.spiritswap.finance/#/pool")
    WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.ID, "join-pool-button"))).click()
    driver.find_element_by_class_name("sc-cvJHqN.kSAZHn.open-currency-select-button").click()

    try: 
        driver.find_element_by_xpath("//div[@title='" + coin[0] + "']").click()
    except NoSuchElementException:
        WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,"//*[contains(text(), '" + coin[0] + "')]"))).click()
    driver.find_element_by_xpath("//*[contains(text(), 'Select a currency')]").click()
    
    time.sleep(1)

    try: 
        driver.find_element_by_xpath("//div[@title='" + coin[1] + "']").click()
    except NoSuchElementException:
        WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,"//*[contains(text(), '" + coin[1] + "')]"))).click()

    time.sleep(2)
    Maxs = driver.find_elements_by_xpath("//*[contains(text(), 'MAX')]")
    
    Maxs[1].click()
    time.sleep(5)

    #find supply button and switch which max it presses if insufficient balance error is displayed
    try:
        driver.find_element_by_class_name("sc-dlfnbm.jkKzPD").click()
    except NoSuchElementException:
        Maxs[0].click()
        WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.CLASS_NAME,"sc-dlfnbm.jkKzPD"))).click()
    
    time.sleep(5)
    confirmSupplyButton = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Confirm Supply')]")))
    confirmSupplyButton.click()

    time.sleep(2)
    try:
        driver.switch_to_window(driver.window_handles[1])
    except:
        closeButton = driver.find_element_by_class_name("sc-bdfBwQ.hjcEfk")
        closeButton.click()
        confirmSupplyButton = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Confirm Supply')]"))).click()
        driver.switch_to_window(driver.window_handles[1])
    
    metamaskConfirm = driver.find_element_by_xpath("//*[contains(text(), 'Confirm')]")
    metamaskConfirm.click()
    time.sleep(10)
    driver.switch_to_window(driver.window_handles[0])

def depositLiquidity(compoundPool):
    driver.get("https://app.spiritswap.finance/#/farms")

    locateCompoundPool = driver.find_element_by_xpath("//*[contains(text(), '" + compoundPool + " LP')]")
    parent = locateCompoundPool.find_element_by_xpath("./../../..")
    
    depositLiquidityButton = WebDriverWait(parent, 60).until(ec.element_to_be_clickable((By.CLASS_NAME,"sc-dlfnbm.ecdXzy.sc-hKgILt.fwjcww")))
    depositLiquidityButton.click()
    
    maxButton = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Max')]")))
    maxButton.click()
    
    confirmLiqDeposit = driver.find_element_by_xpath("//*[contains(text(), 'Confirm')]")
    confirmLiqDeposit.click()
    
    time.sleep(5)
    driver.switch_to_window(driver.window_handles[1])
    metamaskConfirm = driver.find_element_by_xpath("//*[contains(text(), 'Confirm')]")
    metamaskConfirm.click()
    time.sleep(10)
    driver.switch_to_window(driver.window_handles[0])


def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)
    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 2px solid red;")
    time.sleep(.3)
    apply_style(original_style)


print("How many pools are you currently staking LP in on spiritswap?")
numPools = int(input())

print("which pool would you like to compound your earnings into? (Please enter the coin symbols as they appear on the pool ie 'SPIRIT-FTM' with the dash '-' in between)")
compoundPool = str(raw_input())
coins = compoundPool.split('-')

print("How often do you want to compound? (type a number in minutes)")
compoundFreq = int(input())
compoundFreqSec = compoundFreq * 60

driver = startChrome()
connectWalletToSpirit()

for x in range(100):
    totalGasFees = spiritHarvest(numPools)
    time.sleep(10)
    give2percentToGas()
    swapHalf(coins)
    addLiquidity(coins)
    depositLiquidity(compoundPool)
    time.sleep(compoundFreqSec)
