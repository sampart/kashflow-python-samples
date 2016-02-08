# uses SUDS SOAP client: https://fedorahosted.org/suds/
from suds.client import Client
import logging

client = Client("https://securedwebapp.com/api/service.asmx?WSDL")
result = client.service.GetCustomers(UserName="username", Password="username")

print result
