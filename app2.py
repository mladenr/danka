import datetime
import collections


def main():
    bill_list = create_bill_list()
    payment_list = create_payment_list()

    for project_id, bill_by_project_group in group_bill_by_project(bill_list).items():
        print('# Processing data for project: ' + project_id)
        debt = 0.0
        for bill in bill_by_project_group:
            print('   Processing bill: ' + str(bill['amount']))
            debt = debt + bill['amount']
            print('   Total debt before payment processing: ' + str(debt))
            for payment in group_uplata_by_project(payment_list)[project_id]:
                print('   Processing payment: ' + str(payment['amount']))


def create_bill_list():
    return [
        {'projectId': 'project1', 'createdDate': datetime.date(2019, 1, 1), 'deadlineDate': datetime.date(2019, 1, 1), 'amount': 200, 'isplaceno': False, 'kasnioSaIsplatom': None, 'brojDanaKasnjenja': None, 'dug': None, 'pretplata': None, 'uplataList': None},
        {'projectId': 'project1', 'createdDate': datetime.date(2019, 2, 1), 'deadlineDate': datetime.date(2019, 2, 1), 'amount': 300, 'isplaceno': False, 'kasnioSaIsplatom': None, 'brojDanaKasnjenja': None, 'dug': None, 'pretplata': None, 'uplataList': None},
        {'projectId': 'project2', 'createdDate': datetime.date(2019, 2, 1), 'deadlineDate': datetime.date(2019, 2, 1), 'amount': 400, 'isplaceno': False, 'kasnioSaIsplatom': None, 'brojDanaKasnjenja': None, 'dug': None, 'pretplata': None, 'uplataList': None}

    ]


def create_payment_list():
    return [
        {'projectId': 'project1', 'date': datetime.date(2019, 1, 12), 'amount': 1000, 'processed': True}
    ]


def group_bill_by_project(bill_list):
    grouped_bill_by_project = collections.defaultdict(list)
    for item in bill_list:
        grouped_bill_by_project[item['projectId']].append(item)
    for project_id, bill_by_project_group in grouped_bill_by_project.items():
        print
        print(project_id)
        print(bill_by_project_group)
    return grouped_bill_by_project


def group_uplata_by_project(uplata_list):
    grouped_uplata_by_project = collections.defaultdict(list)
    for item in uplata_list:
        grouped_uplata_by_project[item['projectId']].append(item)
    for project_id, uplata_by_project_group in grouped_uplata_by_project.items():
        print
        print(project_id)
        print(uplata_by_project_group)
    return grouped_uplata_by_project


main()
