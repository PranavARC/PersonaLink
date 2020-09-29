from flask import Flask, request, redirect, url_for, render_template, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import mbti2
import dnd2

app = Flask(__name__)

@app.route('/')
def main():
    return(redirect(url_for("dndPg")))

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
        print(dnd2.dndSubmit(dnd2.headlessDND(), opinions))

    driver = dnd2.headlessDND()
    arr = dnd2.dndScrape(driver)
    driver.quit()
    j = 0
    for i in arr:
        nums.append(j)
        j += 1
    return render_template("dnd.html", qs = arr, nums = nums)

if __name__ == "__main__":
    app.run(debug=True)