import datetime
import collections
import pprint


class PaymentsProcessor():
    def main(self):
        bill_list = PaymentsProcessor.create_bill_list()
        payment_list = PaymentsProcessor.create_payment_list()

        for project_id, bill_by_project_group in PaymentsProcessor.group_bill_by_project(bill_list).items():
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

                project_payments = PaymentsProcessor.group_uplata_by_project(payment_list)[project_id]
                total_project_debt = PaymentsProcessor.process_next_payment(bill, project_payments, total_project_debt)

                print('   Total bill debt after payments processing: ' + str(bill['billDebt']))
                print('   Bill isPaidOff: ' + str(bill['isPaidOff']))
                print('   ----------------------------')

        print('Total project debt: ' + str(total_project_debt))
        self.print_results(bill_list, payment_list)

    @staticmethod
    def create_bill_list():
        return [
            {'projectId': 'project1', 'createdDate': datetime.date(2019, 1, 1), 'deadlineDate': datetime.date(2019, 1, 10), 'amount': 200, 'paidAmount': 0, 'paidOver': 0, 'isPaidOff': False, 'lastPaymentDate': None, 'delayInPayment': None, 'daysOfDelay': None, 'totalDebt': None, 'pretplata': None, 'relatedPayments': []},
            {'projectId': 'project1', 'createdDate': datetime.date(2019, 2, 1), 'deadlineDate': datetime.date(2019, 2, 10), 'amount': 300, 'paidAmount': 0, 'paidOver': 0, 'isPaidOff': False, 'lastPaymentDate': None, 'delayInPayment': None, 'daysOfDelay': None, 'totalDebt': None, 'pretplata': None, 'relatedPayments': []},
            {'projectId': 'project1', 'createdDate': datetime.date(2019, 3, 1), 'deadlineDate': datetime.date(2019, 3, 10), 'amount': 400, 'paidAmount': 0, 'paidOver': 0, 'isPaidOff': False, 'lastPaymentDate': None, 'delayInPayment': None, 'daysOfDelay': None, 'totalDebt': None, 'pretplata': None, 'relatedPayments': []}

        ]

    @staticmethod
    def create_payment_list():
        return [
            {'projectId': 'project1', 'date': datetime.date(2019, 1, 12), 'amount': 190, 'processed': False},
            {'projectId': 'project1', 'date': datetime.date(2019, 1, 14), 'amount': 300, 'processed': False},
            {'projectId': 'project1', 'date': datetime.date(2019, 1, 15), 'amount': 500, 'processed': False}
        ]

    @staticmethod
    def group_bill_by_project(bill_list):
        grouped_bill_by_project = collections.defaultdict(list)
        for item in bill_list:
            grouped_bill_by_project[item['projectId']].append(item)
#        for project_id, bill_by_project_group in grouped_bill_by_project.items():
#            print
#            print(project_id)
#            print(bill_by_project_group)
        return grouped_bill_by_project

    @staticmethod
    def group_uplata_by_project(uplata_list):
        grouped_uplata_by_project = collections.defaultdict(list)
        for item in uplata_list:
            grouped_uplata_by_project[item['projectId']].append(item)
#        for project_id, uplata_by_project_group in grouped_uplata_by_project.items():
#            print
#            print(project_id)
#            print(uplata_by_project_group)
        return grouped_uplata_by_project

    @staticmethod
    def find(f, seq):
        """Return first item in sequence where f(item) == True."""
        for item in seq:
            if f(item):
                return item

    @staticmethod
    def process_next_payment(bill, payments, total_project_debt):
        first_not_processed_payment = PaymentsProcessor.find(lambda payment: not payment['processed'], payments)
        if first_not_processed_payment is not None:
            print('      Next payment exists: ' + str(first_not_processed_payment['amount']))
            bill['paidAmount'] = bill['paidAmount'] + first_not_processed_payment['amount']
            bill['billDebt'] = bill['billDebt'] - first_not_processed_payment['amount']
            total_project_debt = total_project_debt - first_not_processed_payment['amount']
            first_not_processed_payment['processed'] = True
            bill['relatedPayments'].append(first_not_processed_payment)
            bill['isPaidOff'] = (bill['billDebt'] <= 0)
            bill['lastPaymentDate'] = first_not_processed_payment['date']
            bill['delayInPayment'] = (bill['lastPaymentDate'] > bill['deadlineDate'])
            if bill['delayInPayment']:
                bill['daysOfDelay'] = (bill['deadlineDate'] - bill['lastPaymentDate']).days
            if bill['billDebt'] > 0:
                total_project_debt = PaymentsProcessor.process_next_payment(bill, payments, total_project_debt)
            if bill['billDebt'] < first_not_processed_payment['amount']:
                bill['paidOver'] = first_not_processed_payment['amount'] - bill['billDebt']
        else:
            print('      Next payment doesnt exist')
        return total_project_debt

    @staticmethod
    def print_results(bills, payments):
        print()
        print('PROCESSED BILLS:')
        pprint.pprint(bills)
        print()
        print('PROCESSED PAYMENTS:')
        pprint.pprint(payments)


if __name__ == '__main__':
    PaymentsProcessor().main()
