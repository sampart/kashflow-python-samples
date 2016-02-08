# uses SUDS SOAP client: https://fedorahosted.org/suds/
from suds.client import Client

import logging
# uncomment these as required for quick access to the code for changing logging level
#logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
#logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)

import os, csv

KASHFLOW_API_WSDL = "https://securedwebapp.com/api/service.asmx?WSDL"
KASHFLOW_USERNAME = "username"
KASHFLOW_PASSWORD = "password"

# helper method - takes an object structured like the following (doesn't need to be a BankTransaction) and returns a list of keys
'''
(BankTransaction){
   ID = 12345678
   accid = 123456
   TransactionDate = 2001-12-17 00:00:00
   moneyin = 1007.5
   moneyout = 0.0
   Vatable = 0
   VatRate = 0.0
   VatAmount = 0.0
   TransactionType = 1234567
   Comment = "comment here"
   ProjectID = 0
   CustomerId = 0
   SupplierId = 0
 }
'''
def createCSVHeaders(instance_obj):
    key_list = []
    for entry in instance_obj:
        key_list.append(entry[0])
    
    # fix for this bug: http://support.microsoft.com/kb/323626
    if key_list[0] == "ID":
        key_list[0] = "'ID"
    
    return key_list

# todo - in anything other than a proof-of-concept, the code here would need to be more robust, checking that values are actually present rather than hard-coding array indices. 

client = Client(KASHFLOW_API_WSDL)
service = client.service
bank_accounts = service.GetBankAccounts(UserName=KASHFLOW_USERNAME, Password=KASHFLOW_PASSWORD)
bank_transactions = service.GetBankTransactions(UserName=KASHFLOW_USERNAME, Password=KASHFLOW_PASSWORD, AccountID=bank_accounts.GetBankAccountsResult[0][0].AccountID)

#print bank_accounts
#print bank_transactions

filename = KASHFLOW_USERNAME + " - " + bank_accounts.GetBankAccountsResult[0][0].AccountName + ".csv"
f = open(filename, 'wb') # must be binary mode - see http://docs.python.org/library/csv.html
csv_writer = csv.writer(f, dialect=csv.excel)

# NB in Python 2.7+, there is a specific DictWriter.writeheader() method which you may wish to use instead - see http://docs.python.org/library/csv.html 
csv_writer.writerow(createCSVHeaders(bank_transactions.GetBankTransactionsResult[0][0])) # pass in a sample entry and write out the header row

csv_writer.writerows(bank_transactions.GetBankTransactionsResult[0])
f.close()

print "%s written" % filename
