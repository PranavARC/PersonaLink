from flask import Flask, request, redirect, url_for, render_template, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import mbti2

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
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

if __name__ == "__main__":
    app.run(debug=True)