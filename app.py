from flask import Flask, render_template, jsonify, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from sqlalchemy import inspect


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite3'

db = SQLAlchemy(app)


class AssetHoldings(db.Model):
    # Defines the Table Name
    __tablename__ = "AssetHoldings"

    # Makes columns into the table
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_name = db.Column(db.String(100), nullable=False)
    inst_name = db.Column(db.String(100), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    asset_name = db.Column(db.String(100), nullable=False)
    asset_type = db.Column(db.String(100), nullable=False)
    shares = db.Column(db.Float(100), nullable=False)
    fmv = db.Column(db.Float(100), nullable=False)
    cv = db.Column(db.Float(100), nullable=False)

    def __init__(self, case_name, inst_name, account_name, date, asset_name, asset_type, shares, fmv, cv):
        self.case_name = case_name
        self.inst_name = inst_name
        self.account_name = account_name
        self.date = date
        self.asset_name = asset_name
        self.asset_type = asset_type
        self.shares = shares
        self.fmv = fmv
        self.cv = cv


class FinancialTransactions(db.Model):
    # Defines the Table Name
    __tablename__ = "FinancialTransactions"

    # Makes columns into the table
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_name = db.Column(db.String(100), nullable=False)
    inst_name = db.Column(db.String(100), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    payee = db.Column(db.String(100), nullable=False)
    check_no = db.Column(db.Float(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    memo = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float(100), nullable=False)
    asset_name = db.Column(db.String(100), nullable=False)
    shares = db.Column(db.Float(100), nullable=False)

    def __init__(self, case_name, inst_name, account_name, date, payee, check_no, category, memo, amount, asset_name, shares):
        self.case_name = case_name
        self.inst_name = inst_name
        self.account_name = account_name
        self.date = date
        self.payee = payee
        self.check_no = check_no
        self.category = category
        self.memo = memo
        self.amount = amount
        self.asset_name = asset_name
        self.shares = shares


class ArchivedAssetHoldings(db.Model):
    # Defines the Table Name
    __tablename__ = "ArchivedAssetHoldings"

    # Makes columns into the table
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_name = db.Column(db.String(100), nullable=False)
    inst_name = db.Column(db.String(100), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    asset_name = db.Column(db.String(100), nullable=False)
    asset_type = db.Column(db.String(100), nullable=False)
    shares = db.Column(db.Float(100), nullable=False)
    fmv = db.Column(db.Float(100), nullable=False)
    cv = db.Column(db.Float(100), nullable=False)

    def __init__(self, case_name, inst_name, account_name, date, asset_name, asset_type, shares, fmv, cv):
        self.case_name = case_name
        self.inst_name = inst_name
        self.account_name = account_name
        self.date = date
        self.asset_name = asset_name
        self.asset_type = asset_type
        self.shares = shares
        self.fmv = fmv
        self.cv = cv


class ArchivedFinancialTransactions(db.Model):
    # Defines the Table Name
    __tablename__ = "ArchivedFinancialTransactions"

    # Makes columns into the table
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_name = db.Column(db.String(100), nullable=False)
    inst_name = db.Column(db.String(100), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    payee = db.Column(db.String(100), nullable=False)
    check_no = db.Column(db.Float(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    memo = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float(100), nullable=False)
    asset_name = db.Column(db.String(100), nullable=False)
    shares = db.Column(db.Float(100), nullable=False)

    def __init__(self, case_name, inst_name, account_name, date, payee, check_no, category, memo, amount, asset_name, shares):
        self.case_name = case_name
        self.inst_name = inst_name
        self.account_name = account_name
        self.date = date
        self.payee = payee
        self.check_no = check_no
        self.category = category
        self.memo = memo
        self.amount = amount
        self.asset_name = asset_name
        self.shares = shares


@app.route("/")
def home():
    return redirect(url_for('holding'))


@app.route("/holding", methods=["GET", "POST"])
def holding():
    # When a user clicks submit query button it will come here.
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)

        cols = ['case_name', 'inst_name', 'account_name', 'date',
                'asset_name', 'asset_type', 'shares', 'fmv', 'cv']
        for i in cols:
            if i not in data:
                data[i] = ['All']

        mydict = {}
        for k, v in data.items():
            if v[0] != "All":
                mydict[k] = v[0]

        date_data = []
        if 'date' in mydict:
            result = mydict['date']
            out = result.split('-')
            start = datetime.strptime(out[0], '%d/%m/%Y').date()
            end = datetime.strptime(out[1], '%d/%m/%Y').date()
            date_data.append(start)
            date_data.append(end)
            del mydict['date']

        if len(mydict) == 0 and len(date_data) != 0:
            holding_data = AssetHoldings.query.filter(
                AssetHoldings.date >= date_data[0]).filter(AssetHoldings.date <= date_data[1]).all()
        elif len(mydict) == 0 and len(date_data) == 0:
            holding_data = AssetHoldings.query.all()
        elif len(mydict) != 0 and len(date_data) != 0:
            holding_data = AssetHoldings.query.filter(
                AssetHoldings.date <= date_data[0]).filter(AssetHoldings.date >= date_data[1]).filter(**mydict).all()
        else:
            holding_data = AssetHoldings.query.filter_by(**mydict).all()

        return render_template("holdings.html", holding_data=holding_data)

    else:
        holding_data = AssetHoldings.query.all()
        return render_template("holdings.html", holding_data=holding_data)


@app.route("/transactions", methods=["GET", "POST"])
def transactions():
    # When a user clicks submit query button it will come here.
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)

        cols = ['case_name', 'inst_name', 'account_name', 'date',
                'payee', 'check_no', 'category', 'memo', 'amount', 'asset_name', 'shares']
        for i in cols:
            if i not in data:
                data[i] = ['All']

        mydict = {}
        for k, v in data.items():
            if v[0] != "All":
                mydict[k] = v[0]

        date_data = []
        if 'date' in mydict:
            result = mydict['date']
            out = result.split('-')
            start = datetime.strptime(out[0], '%d/%m/%Y').date()
            end = datetime.strptime(out[1], '%d/%m/%Y').date()
            date_data.append(start)
            date_data.append(end)
            del mydict['date']

        if len(mydict) == 0 and len(date_data) != 0:
            holding_data = FinancialTransactions.query.filter(
                FinancialTransactions.date >= date_data[0]).filter(FinancialTransactions.date <= date_data[1]).all()
        elif len(mydict) == 0 and len(date_data) == 0:
            holding_data = FinancialTransactions.query.all()
        elif len(mydict) != 0 and len(date_data) != 0:
            holding_data = FinancialTransactions.query.filter(
                FinancialTransactions.date <= date_data[0]).filter(FinancialTransactions.date >= date_data[1]).filter(**mydict).all()
        else:
            holding_data = FinancialTransactions.query.filter_by(
                **mydict).all()

        return render_template("transactions.html", holding_data=holding_data)

    else:
        holding_data = FinancialTransactions.query.all()
        return render_template("transactions.html", holding_data=holding_data)


@ app.route("/archivedholdings", methods=["GET", "POST"])
def archivedholdings():
    # When a user clicks submit query button it will come here.
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)

        cols = ['case_name', 'inst_name', 'account_name', 'date',
                'asset_name', 'asset_type', 'shares', 'fmv', 'cv']
        for i in cols:
            if i not in data:
                data[i] = ['All']

        mydict = {}
        for k, v in data.items():
            if v[0] != "All":
                mydict[k] = v[0]

        date_data = []
        if 'date' in mydict:
            result = mydict['date']
            out = result.split('-')
            start = datetime.strptime(out[0], '%d/%m/%Y').date()
            end = datetime.strptime(out[1], '%d/%m/%Y').date()
            date_data.append(start)
            date_data.append(end)
            del mydict['date']

        if len(mydict) == 0 and len(date_data) != 0:
            holding_data = ArchivedAssetHoldings.query.filter(
                ArchivedAssetHoldings.date >= date_data[0]).filter(ArchivedAssetHoldings.date <= date_data[1]).all()
        elif len(mydict) == 0 and len(date_data) == 0:
            holding_data = ArchivedAssetHoldings.query.all()
        elif len(mydict) != 0 and len(date_data) != 0:
            holding_data = ArchivedAssetHoldings.query.filter(
                ArchivedAssetHoldings.date <= date_data[0]).filter(ArchivedAssetHoldings.date >= date_data[1]).filter(**mydict).all()
        else:
            holding_data = ArchivedAssetHoldings.query.filter_by(
                **mydict).all()

        return render_template("archived_holdings.html", holding_data=holding_data)

    else:
        holding_data = ArchivedAssetHoldings.query.all()
        return render_template("archived_holdings.html", holding_data=holding_data)


@ app.route("/archivedtransactions", methods=["GET", "POST"])
def archivedtransactions():
    # When a user clicks submit query button it will come here.
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)

        cols = ['case_name', 'inst_name', 'account_name', 'date',
                'payee', 'check_no', 'category', 'memo', 'amount', 'asset_name', 'shares']
        for i in cols:
            if i not in data:
                data[i] = ['All']

        mydict = {}
        for k, v in data.items():
            if v[0] != "All":
                mydict[k] = v[0]

        date_data = []
        if 'date' in mydict:
            result = mydict['date']
            out = result.split('-')
            start = datetime.strptime(out[0], '%d/%m/%Y').date()
            end = datetime.strptime(out[1], '%d/%m/%Y').date()
            date_data.append(start)
            date_data.append(end)
            del mydict['date']

        if len(mydict) == 0 and len(date_data) != 0:
            holding_data = ArchivedFinancialTransactions.query.filter(
                ArchivedFinancialTransactions.date >= date_data[0]).filter(ArchivedFinancialTransactions.date <= date_data[1]).all()
        elif len(mydict) == 0 and len(date_data) == 0:
            holding_data = ArchivedFinancialTransactions.query.all()
        elif len(mydict) != 0 and len(date_data) != 0:
            holding_data = ArchivedFinancialTransactions.query.filter(
                ArchivedFinancialTransactions.date <= date_data[0]).filter(ArchivedFinancialTransactions.date >= date_data[1]).filter(**mydict).all()
        else:
            holding_data = ArchivedFinancialTransactions.query.filter_by(
                **mydict).all()

        return render_template("archived_transactions.html", holding_data=holding_data)
    else:
        holding_data = ArchivedFinancialTransactions.query.all()
        return render_template("archived_transactions.html", holding_data=holding_data)


@ app.route("/deleteholdings", methods=['GET', 'POST'])
def deleteholdings():
    output = request.get_json()
    result = json.loads(output)
    data = AssetHoldings.query.filter_by(case_name=result['Case Name']).one()
    AssetHoldings.query.filter_by(case_name=result['Case Name']).delete()
    outp = data.__dict__

    del outp['_sa_instance_state']
    del outp['_id']

    data_obj = ArchivedAssetHoldings(**outp)
    db.session.add(data_obj)
    db.session.commit()

    db.session.commit()

    holding_data = AssetHoldings.query.all()
    return render_template("holdings.html", holding_data=holding_data)


@ app.route("/restoreholdings", methods=['GET', 'POST'])
def restoreholdings():
    output = request.get_json()
    result = json.loads(output)
    data = ArchivedAssetHoldings.query.filter_by(
        case_name=result['Case Name']).one()
    ArchivedAssetHoldings.query.filter_by(
        case_name=result['Case Name']).delete()
    outp = data.__dict__

    del outp['_sa_instance_state']
    del outp['_id']

    data_obj = AssetHoldings(**outp)
    db.session.add(data_obj)
    db.session.commit()

    db.session.commit()

    holding_data = ArchivedAssetHoldings.query.all()
    return render_template("archived_holdings.html", holding_data=holding_data)


@ app.route("/deletetransactions", methods=['GET', 'POST'])
def deletetransactions():
    output = request.get_json()
    result = json.loads(output)
    data = FinancialTransactions.query.filter_by(
        case_name=result['Case Name']).one()
    FinancialTransactions.query.filter_by(
        case_name=result['Case Name']).delete()
    outp = data.__dict__

    del outp['_sa_instance_state']
    del outp['_id']

    data_obj = ArchivedFinancialTransactions(**outp)
    db.session.add(data_obj)
    db.session.commit()

    db.session.commit()

    holding_data = FinancialTransactions.query.all()
    return render_template("transactions.html", holding_data=holding_data)


@ app.route("/restoretransactions", methods=['GET', 'POST'])
def restoretransactions():
    output = request.get_json()
    result = json.loads(output)
    data = ArchivedFinancialTransactions.query.filter_by(
        case_name=result['Case Name']).one()
    ArchivedFinancialTransactions.query.filter_by(
        case_name=result['Case Name']).delete()
    outp = data.__dict__

    del outp['_sa_instance_state']
    del outp['_id']

    data_obj = FinancialTransactions(**outp)
    db.session.add(data_obj)
    db.session.commit()

    db.session.commit()

    holding_data = ArchivedFinancialTransactions.query.all()
    return render_template("archived_transactions.html", holding_data=holding_data)


@ app.route("/addholdings", methods=['GET', 'POST'])
def addholdings():
    output = request.get_json()
    result = json.loads(output)

    date = result['Date Range']
    newdate = datetime.strptime(date, "%d/%m/%Y").date()
    result['Date Range'] = newdate

    shares = result['Shares']
    newshares = float(shares)
    result['Shares'] = newshares

    fmv = result['FMV']
    newfmv = float(fmv)
    result['FMV'] = newfmv

    cv = result['CV']
    newcv = float(cv)
    result['CV'] = newcv

    data = []
    for v in result.values():
        data.append(v)

    data_obj = AssetHoldings(*data)
    db.session.add(data_obj)
    db.session.commit()

    return redirect(url_for('holding'))


@ app.route("/addtransactions", methods=['GET', 'POST'])
def addtransactions():
    output = request.get_json()
    result = json.loads(output)

    date = result['Date Range']
    newdate = datetime.strptime(date, "%d/%m/%Y").date()
    result['Date Range'] = newdate

    shares = result['Shares']
    newshares = float(shares)
    result['Shares'] = newshares

    check_no = result['Check No.']
    newcheck_no = float(check_no)
    result['Check No.'] = newcheck_no

    amount = result['Amount']
    newamount = float(amount)
    result['Amount'] = amount

    data = []
    for v in result.values():
        data.append(v)

    data_obj = FinancialTransactions(*data)
    db.session.add(data_obj)
    db.session.commit()

    return redirect(url_for('transactions'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
