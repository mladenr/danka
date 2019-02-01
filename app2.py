import datetime
import collections
import pprint

class PaymentsProcessor():
    def main(self):
        bill_list = self.create_bill_list()
        payment_list = self.create_payment_list()

        for project_id, bill_by_project_group in self.group_bill_by_project(bill_list).items():
            print('********************************')
            print('# Processing data for project: ' + project_id)
            print('********************************')

            total_project_debt = 0.0
            for bill in bill_by_project_group:
                print('   ----------------------------')
                print('   Processing bill: ' + str(bill['amount']))

                bill['billDebt'] = bill['amount']
                total_project_debt = total_project_debt + bill['amount']

                print('   Total project debt before payment processing: ' + str(total_project_debt))
                print('   Total bill debt before payment processing: ' + str(bill['billDebt']))

                project_payments = self.group_uplata_by_project(payment_list)[project_id]
                total_project_debt = self.process_next_payment(bill, project_payments, total_project_debt)

                print('   Total bill debt after payments processing: ' + str(bill['billDebt']))
                print('   Bill isPaidOff: ' + str(bill['isPaidOff']))
                print('   ----------------------------')

        print('Total project debt: ' + str(total_project_debt))
        self.print_results(bill_list, payment_list)


    def create_bill_list(self):
        return [
            {'projectId': 'project1', 'createdDate': datetime.date(2019, 1, 1), 'deadlineDate': datetime.date(2019, 1, 10), 'amount': 200, 'paidAmount': 0, 'paidOver': 0, 'isPaidOff': False, 'lastPaymentDate': None, 'delayInPayment': None, 'daysOfDelay': None, 'totalDebt': None, 'pretplata': None, 'relatedPayments': []},
            {'projectId': 'project1', 'createdDate': datetime.date(2019, 2, 1), 'deadlineDate': datetime.date(2019, 2, 10), 'amount': 300, 'paidAmount': 0, 'paidOver': 0, 'isPaidOff': False, 'lastPaymentDate': None, 'delayInPayment': None, 'daysOfDelay': None, 'totalDebt': None, 'pretplata': None, 'relatedPayments': []},
            {'projectId': 'project1', 'createdDate': datetime.date(2019, 3, 1), 'deadlineDate': datetime.date(2019, 3, 10), 'amount': 400, 'paidAmount': 0, 'paidOver': 0, 'isPaidOff': False, 'lastPaymentDate': None, 'delayInPayment': None, 'daysOfDelay': None, 'totalDebt': None, 'pretplata': None, 'relatedPayments': []}

        ]


    def create_payment_list(self):
        return [
            {'projectId': 'project1', 'date': datetime.date(2019, 1, 12), 'amount': 190, 'processed': False, 'unpaidAmount': None},
            {'projectId': 'project1', 'date': datetime.date(2019, 1, 14), 'amount': 300, 'processed': False, 'unpaidAmount': None},
            {'projectId': 'project1', 'date': datetime.date(2019, 1, 15), 'amount': 500, 'processed': False, 'unpaidAmount': None}
        ]


    def group_bill_by_project(self, bill_list):
        grouped_bill_by_project = collections.defaultdict(list)
        for item in bill_list:
            grouped_bill_by_project[item['projectId']].append(item)
        for project_id, bill_by_project_group in grouped_bill_by_project.items():
            print
#            print(project_id)
#            print(bill_by_project_group)
        return grouped_bill_by_project


    def group_uplata_by_project(self, uplata_list):
        grouped_uplata_by_project = collections.defaultdict(list)
        for item in uplata_list:
            grouped_uplata_by_project[item['projectId']].append(item)
        for project_id, uplata_by_project_group in grouped_uplata_by_project.items():
            print
#            print(project_id)
#            print(uplata_by_project_group)
        return grouped_uplata_by_project

    def find(self, f, seq):
        """Return first item in sequence where f(item) == True."""
        for item in seq:
            if f(item):
                return item


    def process_next_payment(self, bill, payments, total_project_debt):
        firstNotProcessedPayment = self.find(lambda payment: not payment['processed'], payments)
        if firstNotProcessedPayment is not None:
            if (firstNotProcessedPayment['unpaidAmount'] is None):
                amount = firstNotProcessedPayment['amount']
            else:
                amount = firstNotProcessedPayment['unpaidAmount']

            if (amount > bill['billDebt']):
                chargeFromPayment = bill['billDebt']
                firstNotProcessedPayment['unpaidAmount'] = amount - bill['billDebt']
            else:
                chargeFromPayment = amount
                firstNotProcessedPayment['unpaidAmount'] = 0
                firstNotProcessedPayment['processed'] = True

            bill['paidAmount'] = bill['paidAmount'] + chargeFromPayment
            bill['billDebt'] = bill['billDebt'] - chargeFromPayment
            total_project_debt = total_project_debt - chargeFromPayment
            bill['relatedPayments'].append(firstNotProcessedPayment)
            bill['isPaidOff'] = (bill['billDebt'] <= 0)
            bill['lastPaymentDate'] = firstNotProcessedPayment['date']
            bill['delayInPayment'] = (bill['lastPaymentDate'] > bill['deadlineDate'])
            if (bill['delayInPayment']):
                bill['daysOfDelay'] = (bill['deadlineDate'] - bill['lastPaymentDate']).days
            if (bill['billDebt'] > 0):
                total_project_debt = self.process_next_payment(bill, payments, total_project_debt)
            if (bill['billDebt'] < firstNotProcessedPayment['amount']):
                bill['paidOver'] = firstNotProcessedPayment['amount'] - bill['billDebt']

        else:
            print('      Next payment doesnt exist')
        return total_project_debt


    def print_results(self, bills, payments):
        print()
        print('PROCESSED BILLS:')
        pprint.pprint(bills)
        print()
        print('PROCESSED PAYMENTS:')
        pprint.pprint(payments)


if __name__ == '__main__':
    PaymentsProcessor().main()
