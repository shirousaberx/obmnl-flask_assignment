# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route('/')
def get_transactions():
    return render_template('transactions.html', transactions=transactions)

# Create operation
@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }

        transactions.append(transaction)

        return redirect(url_for('get_transactions'))

    return render_template('form.html')

# Update operation
@app.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = request.form['date']
                transaction['amount'] = float(request.form['amount'])
                return redirect(url_for('get_transactions'))
        else:
            return {'message': 'transaction_id not found'}, 404


    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template('edit.html', transaction=transaction)
    else:
        return {'message': 'transaction_id not found'}, 404

# Delete operation
@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            return redirect(url_for('get_transactions'))
    else:
        return {'message': 'transaction_id not found'}, 404

@app.route('/search', methods=['GET', 'POST'])
def search_transaction():
    if request.method == 'POST':
        min_amount = request.form.get('min_amount')
        max_amount = request.form.get('max_amount')

        if not (min_amount and max_amount):
            return {'message': 'min_amount or max_amount is empty'}, 404

        min_amount = float(min_amount)
        max_amount = float(max_amount)
        temp_trans = []
        for transaction in transactions:
            if transaction['amount'] <= max_amount and transaction['amount'] >= min_amount:
                temp_trans.append(transaction)
        
        return render_template('transactions.html', transactions=temp_trans)

    return render_template('search.html')

@app.route('/balance')
def total_balance():
    balance = 0
    for transaction in transactions:
        balance += transaction['amount']
    
    return render_template('transactions.html', transactions=transactions, total_balance=balance)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)