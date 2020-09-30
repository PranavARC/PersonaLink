from flask import Flask, request, redirect, url_for, render_template, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import functions2

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
        driverM = functions2.headless(0)
        print(functions2.mbtiSubmit(driverM, opinions))
        driverM.quit()

    driver = functions2.headless(0)
    arr = functions2.mbtiScrape(driver)
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
        driver = functions2.headless(1)
        print(functions2.dndSubmit(driver, opinions))
        driver.quit()

    driver = functions2.headless(1)
    arr = functions2.dndScrape(driver)
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
        driver = functions2.headless(2)
        print(functions2.gramSubmit(driver, opinions))
        driver.quit()
    
    driver = functions2.headless(2)
    arr = functions2.gramScrape(driver)
    driver.quit()
    j = 0
    for i in arr[0]:
        nums.append(j)
        j += 1    
    return render_template("gram.html", qs = arr, nums = nums)


if __name__ == "__main__":
    app.run(debug=True)