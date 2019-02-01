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
            debt = 0.0
            for bill in bill_by_project_group:
                print('   ----------------------------')
                print('   Processing bill: ' + str(bill['amount']))
                debt = debt + bill['amount']
                print('   Total debt before payment processing: ' + str(debt))
                project_payments = self.group_uplata_by_project(payment_list)[project_id]
                response = self.process_next_payment(bill, project_payments, debt)
                if (response is not None):
                    debt = response['debt']
                    lastPaymentDate = response['lastPaymentDate']
                    print('      Total debt after payments processing: ' + str(debt))
                    if (debt == 0):
                        bill['isplaceno'] = True
                        bill['debt'] = 0
                        bill['pretplata'] = 0
                        bill['delayInPayment'] = (lastPaymentDate > bill['deadlineDate'])
                        if (bill['delayInPayment']):
                            bill['daysOfDelay'] = (bill['deadlineDate'] - lastPaymentDate).days
                    elif (debt > 0):
                        bill['isplaceno'] = False
                        bill['debt'] = debt
                        bill['pretplata'] = 0
                    else:
                        bill['isplaceno'] = True
                        bill['debt'] = 0
                        bill['pretplata'] = abs(debt)
                        bill['delayInPayment'] = (lastPaymentDate > bill['deadlineDate'])
                        if (bill['delayInPayment']):
                            bill['daysOfDelay'] = (bill['deadlineDate'] - lastPaymentDate).days
                print('   ----------------------------')
        self.print_results(bill_list, payment_list)


    def create_bill_list(self):
        return [
            {'projectId': 'project1', 'createdDate': datetime.date(2019, 1, 1), 'deadlineDate': datetime.date(2019, 1, 10), 'amount': 200, 'isplaceno': False, 'delayInPayment': None, 'daysOfDelay': None, 'debt': None, 'pretplata': None, 'relatedPayments': []},
            {'projectId': 'project1', 'createdDate': datetime.date(2019, 2, 1), 'deadlineDate': datetime.date(2019, 2, 10), 'amount': 300, 'isplaceno': False, 'delayInPayment': None, 'daysOfDelay': None, 'debt': None, 'pretplata': None, 'relatedPayments': []},
            {'projectId': 'project2', 'createdDate': datetime.date(2019, 3, 1), 'deadlineDate': datetime.date(2019, 3, 10), 'amount': 400, 'isplaceno': False, 'delayInPayment': None, 'daysOfDelay': None, 'debt': None, 'pretplata': None, 'relatedPayments': []}

        ]


    def create_payment_list(self):
        return [
            {'projectId': 'project1', 'date': datetime.date(2019, 1, 12), 'amount': 50, 'processed': False},
            {'projectId': 'project1', 'date': datetime.date(2019, 1, 14), 'amount': 130, 'processed': False},
            {'projectId': 'project1', 'date': datetime.date(2019, 1, 15), 'amount': 100, 'processed': False}
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


    def process_next_payment(self, bill, payments, debt):
        firstNotProcessedPayment = self.find(lambda payment: not payment['processed'], payments)
        response = None
        payment_date = None
        newDebt = debt
        if firstNotProcessedPayment is not None:
            print('      Next payment exists: ' + str(firstNotProcessedPayment['amount']))
            firstNotProcessedPayment['processed'] = True
            bill['relatedPayments'].append(firstNotProcessedPayment)
            debt = debt - firstNotProcessedPayment['amount']
            print('      New debt: ' + str(debt))
            if (debt <= 0):
                payment_date = firstNotProcessedPayment['date']
            else:
                response = self.process_next_payment(bill, payments, debt)
                if (response is not None):
                    debt = response['debt']
                    payment_date = response['lastPaymentDate']
            response = {"debt": debt, "lastPaymentDate": payment_date}
        else:
            print('      Next payment doesnt exist')
        return response


    def print_results(self, bills, payments):
        print()
        print('PROCESSED BILLS:')
        pprint.pprint(bills)
        print()
        print('PROCESSED PAYMENTS:')
        pprint.pprint(payments)


if __name__ == '__main__':
    PaymentsProcessor().main()
