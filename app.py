import pprint
from dataloader import DataLoader
from utils import GroupUtils


class PaymentsProcessor:
    def main(self):
        bill_list = DataLoader.load_bill_list_from_excel()
        payment_list = DataLoader.load_payment_list_from_excel()

        for project_id, bill_by_project_group in GroupUtils.group_bill_by_project(bill_list).items():
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

                project_payments = GroupUtils.group_payment_by_project(payment_list)[project_id]
                total_project_debt = PaymentsProcessor.process_bill(bill, project_payments, total_project_debt)

                print('   Total bill debt after payments processing: ' + str(bill['billDebt']))
                print('   Bill isPaidOff: ' + str(bill['isPaidOff']))
                print('   ----------------------------')

        print('Total project debt: ' + str(total_project_debt))
        self.print_results(bill_list, payment_list)

    @staticmethod
    def find(f, seq):
        """Return first item in sequence where f(item) == True."""
        for item in seq:
            if f(item):
                return item

    @staticmethod
    def process_bill(bill, payments, total_project_debt):
        first_not_processed_payment = PaymentsProcessor.find(lambda payment: not payment['processed'], payments)
        if first_not_processed_payment is not None:
            print('      Next payment exists: ' + str(first_not_processed_payment['amount']))
            if first_not_processed_payment['unpaidAmount'] is None:
                amount = first_not_processed_payment['amount']
            else:
                amount = first_not_processed_payment['unpaidAmount']

            if amount > bill['billDebt']:
                charge_from_payment = bill['billDebt']
                first_not_processed_payment['unpaidAmount'] = amount - bill['billDebt']
            else:
                charge_from_payment = amount
                first_not_processed_payment['unpaidAmount'] = 0
                first_not_processed_payment['processed'] = True

            bill['paidAmount'] = bill['paidAmount'] + charge_from_payment
            bill['billDebt'] = bill['billDebt'] - charge_from_payment
            total_project_debt = total_project_debt - charge_from_payment
            bill['relatedPayments'].append(first_not_processed_payment)
            bill['isPaidOff'] = (bill['billDebt'] <= 0)
            bill['lastPaymentDate'] = first_not_processed_payment['date']
            bill['delayInPayment'] = (bill['lastPaymentDate'] > bill['deadlineDate'])
            if bill['delayInPayment']:
                bill['daysOfDelay'] = (bill['deadlineDate'] - bill['lastPaymentDate']).days
            if bill['billDebt'] > 0:
                total_project_debt = PaymentsProcessor.process_bill(bill, payments, total_project_debt)
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
