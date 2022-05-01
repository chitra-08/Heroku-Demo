from flask import Flask, render_template, request, redirect, url_for
import pickle
import sklearn

app = Flask(__name__)
model = pickle.load(open("loanApplicant_lr1.pkl", "rb"))
loanStatus = ''


@app.route('/thankyou/<status>', methods=['GET', 'POST'])
def thankyou(status):
    print(status)
    return render_template('ThankYou.html', status=status)


@app.route('/')
def home():
    return render_template('LoanApplication.html')


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        fullname = request.form.get('fullName')
        email = request.form.get('email')
        age = float(request.form.get('age'))
        inc = float(request.form.get('income'))
        loan_amt = float(request.form.get('loanamt'))
        prop_value = float(request.form.get('propVal'))
        if request.form['cr_hist'] is not None or request.form['cr_hist'] != 'NA':
            credit_history = int(request.form['cr_hist'])
        if request.form['prop_type'] is not None or request.form['prop_type'] != 'NA':
            prop_type = int(request.form['prop_type'])
        prediction = model.predict([[
            age,
            inc,
            loan_amt,
            credit_history,
            prop_type,
            prop_value
        ]])
        print(prediction)
        output = round(prediction[0])
        global loanStatus
        if output == 1:
            loanStatus = 'approved'
        else:
            loanStatus = 'rejected'
        return redirect(url_for('thankyou', status=loanStatus))

    return render_template('LoanApplication.html')


if __name__ == "__main__":
    app.run(host='140.238.255.177',debug=True)
