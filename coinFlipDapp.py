from flask import Flask, render_template, url_for, flash, redirect
from forms import FlipBetForm
from deploy import DeployContract, FundContract
from coinFlip import coinFlipBet

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = FlipBetForm()
    if form.validate_on_submit():
        result = coinFlipBet(form.betAmt.data)
        if result == 1:
            flash('You won!', 'success')
            return redirect(url_for('home'))
        else:
            flash('You lost :(', 'danger')
            return redirect(url_for('home'))
    return render_template('layout.html', form=form)



if __name__ == '__main__':
    DeployContract()
    FundContract()
    app.run(debug=True)
