from requests import Session
from dataclasses import dataclass, field
from dotenv import load_dotenv
import os
from pprint import pprint as pp
import json
import csv

#  Load variables
load_dotenv()

acc1_id = "10363274"
acc2_id = "10363273"
acc3_id = "10363272"


@dataclass
class Yodlee:
    loginName: str
    access_token: str = ''
    client_id = os.getenv('DEV_CLIENT_ID')
    secret = os.getenv('DEV_SECRET')
    endpoint = os.getenv('DEV_YODLEE_ENDPOINT')
    auth: tuple = field(default=())
    session = Session()
    account_file: str = 'accounts.json'

    def __post_init__(self):
        pass

    def get_access_token(self):
        h = {"Api-Version": "1.1", 'loginName': self.loginName,
             "Content-Type": "application/x-www-form-urlencoded", }
        p = f'clientId={self.client_id}&secret={self.secret}'
        route = '/auth/token'
        self.session.headers.update(h)
        r = self.session.post(
            url=f'{self.endpoint}{route}', data=p)
        token = r.json()
        print(token['token']['accessToken'])
        self.access_token = token['token']['accessToken']
        return

    def get_accounts(self):
        h = {"Api-Version": "1.1", "Authorization": "Bearer " + self.access_token,
             "Content-Type": "application/x-www-form-urlencoded", }
        route = '/accounts'
        self.session.headers.update(h)
        r = self.session.get(
            url=f'{self.endpoint}{route}')
        accounts = r.json()
        return accounts

    def get_account_detail(self, accID):
        h = {"Api-Version": "1.1", "Authorization": "Bearer " + self.access_token,
             "Content-Type": "application/x-www-form-urlencoded", }
        route = f'/accounts/{accID}'
        self.session.headers.update(h)
        r = self.session.get(
            url=f'{self.endpoint}{route}')
        account_details = r.json()
        return account_details

    def get_single_account(self, acc_id: str):
        h = {"Api-Version": "1.1", "Authorization": "Bearer " + self.access_token,
             "Content-Type": "application/x-www-form-urlencoded", }
        route = f'/transactions'
        self.session.headers.update(h)
        pl = f"accountId={acc_id}&top=60"
        r = self.session.get(
            url=f'{self.endpoint}{route}', params=pl)
        account = r.json()
        return account

    def createAccDetailJson(self, accID: str, filename: str):
        with open(filename, 'w') as f:
            data = self.get_account_detail(accID)
            f.write(json.dumps(data, indent=2))

    def createTrasanctionJson(self, accID: str, filename: str):
        with open(filename, 'w') as f:
            data = y.get_single_account(accID)
            f.write(json.dumps(data, indent=2))

    def createAccountsJson(self):
        with open(self.account_file, 'w') as f:
            data = self.get_accounts()
            f.write(json.dumps(data, indent=2))

    def getTransactionsJsonData(self, filename: str):
        with open(filename, 'r') as f:
            data = json.load(f)
            transactions = data['transaction']
        return transactions

    def createCsvFile(self, filename: str):
        with open(filename+'.csv', 'w') as f:
            data = self.getTransactionsJsonData(filename=filename+'.json')
            fieldnames = data[0].keys()
            writer = csv.DictWriter(
                f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            for t in data:
                writer.writerow(t)


y = Yodlee(loginName='rhillz')
