from requests.auth import HTTPBasicAuth
import requests
import re
import argparse
import json
from jira import JIRA
import pandas as pd


'''
create parameter:
user: --u user1,user2,user4,....
group: --g groupname
username_auth: -U username
password_auth: -P password
scheme = [ten_division][groupname]
xlsx_permission_file: --f filename
'''

parser = argparse.ArgumentParser(description='Process some jira automation',  
                                 prog='jira_project',)
parser.add_argument('--g', metavar='--group_name', type=str, nargs='?',
                    help='create new group or add user to group_name if exists', dest='group', required=True)
parser.add_argument('--u', metavar='--username', type=str, nargs='+',
                    help='list of username', dest='users')
parser.add_argument('--f', metavar='--filename', type=str, nargs='?',
                    help='permission file', dest='file')
parser.add_argument('--d', metavar='--divisionname', type=str, nargs='?',
                    help='division name', dest='div', required=True)
parser.add_argument('-U', metavar='-auth_username', type=str, nargs='?',
                    help='username to login jira', dest='username', required=True)
parser.add_argument('-P', metavar='-auth_password', type=str, nargs='?',
                    help='password to login jira', dest='password', required=True)




args = parser.parse_args()
# print(args)
# exit()


FILENAME = args.file
GROUPNAME = args.group.upper()
USERNAME = args.username
PASSWORD = args.password

'''
AUTHENTICATE JIRA INSTANCE
'''

try:
    print("Processing user authentication...")
    jira = JIRA(
        server="https://jira-training.arrowhitech.net",
        basic_auth=(USERNAME, PASSWORD),  # a username/password tuple [Not recommended]
        # basic_auth=("email", "API token"),  # Jira Cloud: a username/token tuple
        # token_auth="",  # Self-Hosted Jira (e.g. Server): the PAT token
        # auth=("admin", "admin"),  # a username/password tuple for cookie auth [Not recommended]
    )
except Exception as ex:
    print("Error on account connection with Jira. Please check again your username or password")
print("Done.\n")

'''
CREATION GROUP AND USE THIS GROUP NAME AS SCHEMENAME
'''

print("Processing group creation...")

try:
    jira.add_group(groupname=GROUPNAME)
    print(f"Created group {GROUPNAME}.")
    print("---------------------------------------------")
except Exception as ex:
    # print(ex)
    print(f"Group {GROUPNAME} already exist")
    print("---------------------------------------------")
        
print("Done.\n")
# exit()

'''
ADD USERS TO GROUP 
'''

if(args.users):
    list_users = []
    USERS = args.users.copy()
    print(f"Adding user to group {GROUPNAME}...\n")
    for user in USERS:
        try:
            response = jira.add_user_to_group(username=user, group=GROUPNAME)
            print(response)
            print(f"Added user {user} to group {GROUPNAME}")
        except Exception as ex:
            result = re.findall(r"'(.*?)'", ex.text)
            response_text = ex.text
            match = response_text.find("already a member")
            if(match != -1):
                pass
            else:
                list_users.append(result[0])
            print(response_text)
            print("---------------------------------------------")

    # print(*list_users)
    print("Done\n")



'''
GRANT PERMISSION
'''

try:
    DIVISIONNAME=args.div.upper()
except Exception as ex:
    print("Missing division name")
    
if (args.file):
    try:
        df = pd.read_excel(FILENAME+".xlsx")
    except Exception as ex:
        print(ex)
        print("Error on reading file. Wrong filename or file extension")
    else:    
        columns = df.columns[0:]
        # permissions = df[columns[0]]
        group_columns = df[columns[1]]
        
    permissions = ['Administer Projects',
                   'Browse Projects',
                   'Edit Sprint name and goal permission',
                   'Manage Sprints permission',
                   'Start stop Sprints permission',
                   'View dev tools',
                   'View readonly workflow',
                   'Assignable User',
                   'Assign Issues',
                   'Close Issues',
                   'Create Issues',
                   'Delete Issues',
                   'Edit Issues',
                   'Link Issues',
                   'Modify Reporter',
                   'Move Issues',
                   'Resolve Issues',
                   'Schedule Issues',
                   'Set Issue Security',
                   'Transition Issues',
                   'Manage Watchers',
                   'View Voters and Watchers',
                   'Add Comments',
                   'Delete All Comments',
                   'Delete Own Comments',
                   'Edit All Comments',
                   'Edit Own Comments',
                   'Create Attachments',
                   'Delete All Attachments',
                   'Delete Own Attachments',
                   'Delete All Worklogs',
                   'Delete Own Worklogs',
                   'Edit All Worklogs',
                   'Edit Own Worklogs',
                   'project Log Work for Others',
                   'project View All Worklogs',
                   'Work On Issues']
    
    all_group = []
    param = []
    json_grants = []
    try:
        for i in range(len(permissions)):
            permission = permissions[i]
            permission = permission.upper()
            permission = permission.split()
            permission = '_'.join(permission)
            groups = group_columns[i]
            groups = groups.split(',')
            for group in groups:
                group = group.strip()
                if group == "Group project":
                    group = GROUPNAME
                param.append([permission, group])
                json_grants.append({
                    "holder":
                    {
                    "type": "group",
                    "parameter": group,
                    },
                    "permission": permission,
                })
    except Exception as ex:
        print("Error on creating JSON PERMISSION GRANT OBJECT")
        
    try:   
        print("Processing granting permissions...")
        url = "http://jira-training.arrowhitech.net/rest/api/2/permissionscheme"

        auth = HTTPBasicAuth(USERNAME, PASSWORD)

        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }
        
        payload = json.dumps({
            "name": DIVISIONNAME + GROUPNAME,
            "description": "Description for this scheme permission",
            "permissions": json_grants,
        })

        response = requests.request(
        "POST",
        url,
        headers=headers,
        auth=auth,
        data=payload,
        )
        
        # print(list_users)
    except Exception as ex:
        print("Error on sending request to grant permissions")
        print(ex.text)
    print("Done.\n")