import collections


class GroupUtils:

    @staticmethod
    def group_bill_by_project(bill_list):
        grouped_bill_by_project = collections.defaultdict(list)
        for item in bill_list: grouped_bill_by_project[item['projectId']].append(item)
        #   for project_id, bill_by_project_group in grouped_bill_by_project.items():
        #       print
        #       print(project_id)
        #       print(bill_by_project_group)
        return grouped_bill_by_project

    @staticmethod
    def group_payment_by_project(payment_list):
        grouped_payment_by_project = collections.defaultdict(list)
        for item in payment_list:
            grouped_payment_by_project[item['projectId']].append(item)
        #   for project_id, payment_by_project_group in grouped_payment_by_project.items():
        #       print
        #       print(project_id)
        #       psrint(payment_by_project_group)
        return grouped_payment_by_project
