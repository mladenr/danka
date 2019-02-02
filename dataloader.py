import datetime
import pandas as pd
import json


class DataLoader:

    @staticmethod
    def create_bill_list():
        return [
            {'projectId': 'project1', 'createdDate': datetime.date(2019, 1, 1), 'deadlineDate': datetime.date(2019, 1, 10), 'amount': 200, 'paidAmount': 0, 'paidOver': 0, 'isPaidOff': False, 'lastPaymentDate': None, 'delayInPayment': None, 'daysOfDelay': None, 'totalDebt': None, 'relatedPayments': []},
            {'projectId': 'project1', 'createdDate': datetime.date(2019, 2, 1), 'deadlineDate': datetime.date(2019, 2, 10), 'amount': 300, 'paidAmount': 0, 'paidOver': 0, 'isPaidOff': False, 'lastPaymentDate': None, 'delayInPayment': None, 'daysOfDelay': None, 'totalDebt': None, 'relatedPayments': []},
            {'projectId': 'project1', 'createdDate': datetime.date(2019, 3, 1), 'deadlineDate': datetime.date(2019, 3, 10), 'amount': 400, 'paidAmount': 0, 'paidOver': 0, 'isPaidOff': False, 'lastPaymentDate': None, 'delayInPayment': None, 'daysOfDelay': None, 'totalDebt': None, 'relatedPayments': []}

        ]

    @staticmethod
    def create_payment_list():
        return [
            {'projectId': 'project1', 'date': datetime.date(2019, 1, 12), 'amount': 190, 'processed': False, 'unpaidAmount': None},
            {'projectId': 'project1', 'date': datetime.date(2019, 1, 14), 'amount': 300, 'processed': False, 'unpaidAmount': None},
            {'projectId': 'project1', 'date': datetime.date(2019, 1, 15), 'amount': 500, 'processed': False, 'unpaidAmount': None}
        ]

    @staticmethod
    def load_bill_list_from_excel():
        data = pd.read_excel('bills.xlsx')
        json_string = data.to_json(orient='records')
        bill_list = json.loads(json_string)
        for bill in bill_list:
            bill['deadlineDate'] = datetime.date.fromtimestamp(bill['deadlineDate'] / 1000)
            bill['paidAmount'] = 0
            bill['relatedPayments'] = []
            bill['lastPaymentDate'] = None
            bill['isPaidOff'] = False
        return sorted(bill_list, key=lambda b: b['createdDate'])

    @staticmethod
    def load_payment_list_from_excel():
        data = pd.read_excel('payments.xlsx')
        json_string = data.to_json(orient='records')
        payment_list = json.loads(json_string)
        for payment in payment_list:
            payment['date'] = datetime.date.fromtimestamp(payment['date'] / 1000)
            payment['processed'] = False
            payment['unpaidAmount'] = None
        return sorted(payment_list, key=lambda b: b['date'])
