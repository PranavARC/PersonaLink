from flask import Flask, request, redirect, url_for, render_template, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import mbti2
import dnd2
import gram2

app = Flask(__name__)

@app.route('/')
def main():
    return(redirect(url_for("gramPg")))

@app.route('/mbti', methods=['GET', 'POST'])
def mbtiPg():
    arr = []
    nums = []

    if request.method == 'POST':
        opinions = []
        for i in range(60):
            opinions.append(int(request.form["opinion"+str(i)]))
        print(opinions)
        driverM = mbti2.headlessMbti()
        print(mbti2.mbtiSubmit(driverM, opinions))
        driverM.quit()

    driver = mbti2.headlessMbti()
    arr = mbti2.mbtiScrape(driver)
    driver.quit()
    j = 0
    for i in arr:
        nums.append(j)
        j += 1
    return render_template("mbti.html", qs = arr, nums = nums)

@app.route('/dnd', methods=['GET', 'POST'])
def dndPg():
    arr = []
    nums = []

    if request.method == 'POST':
        opinions = []
        for i in range(36):
            try:
                val = int(request.form["q"+str(i)])
            except:
                val = 0
            opinions.append(val)
        driver = dnd2.headlessDND()
        print(dnd2.dndSubmit(driver, opinions))
        driver.quit()

    driver = dnd2.headlessDND()
    arr = dnd2.dndScrape(driver)
    driver.quit()
    j = 0
    for i in arr:
        nums.append(j)
        j += 1
    return render_template("dnd.html", qs = arr, nums = nums)

@app.route('/gram', methods=['GET', 'POST'])
def gramPg():
    arr = []
    nums = []

    if request.method == 'POST':
        opinions = [[], []]
        for i in range(52):
            val = request.form["q"+str(i)]
            name = val[:val.find("--")]
            val = int(val[-1])
            opinions[0].append(name)
            opinions[1].append(val)
        # print("Here are the questions and values:")
        # i = 0
        # while i < len(opinions[0]):
        #     print("(" + opinions[0][i] + ") - " + str(opinions[1][i]))
        #     i += 1
        driver = gram2.headlessGram()
        print(gram2.gramSubmit(driver, opinions))
        driver.quit()
    
    driver = gram2.headlessGram()
    arr = gram2.gramScrape(driver)
    driver.quit()
    j = 0
    for i in arr[0]:
        nums.append(j)
        j += 1    
    return render_template("gram.html", qs = arr, nums = nums)


if __name__ == "__main__":
    app.run(debug=True)