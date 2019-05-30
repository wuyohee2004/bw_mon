import requests
from orionsdk import SwisClient
import itchat, time, sys,io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

#https://solarwinds-apac.schneider-electric.com/Orion/Interfaces/InterfaceDetails.aspx?NetObject=I:45156&view=InterfaceDetails
npm_server = 'solarwinds-apac.schneider-electric.com'
username = 'apa\sesa392975'
password = 'Passw0rd17!!'

verify = False

if not verify:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


site_dict = {"SHCF": 45156, "TSDC": 26253, "SHZJ": 44809, "DCSH": 44980, "SECI":45148, "WHRO":45133}

def fatch_in_percentage(intID):
    swis = SwisClient(npm_server, username, password)
    query = """
        SELECT 
        I.InPercentUtil
        FROM
        Orion.NPM.Interfaces I
        WHERE
        I.InterfaceID = %(ID)d
    """
    return swis.query(query % dict(ID=intID))

def main():
    itchat.auto_login(hotReload=True, enableCmdQR=True)
    inPercent_dict = {}
    for key in site_dict:
        result=fatch_in_percentage(site_dict[key])
        data = (result["results"])[0]
        # inPercent_dict[.update(key = data['InPercentUtil'])]
        inPercent_dict[key] = data['InPercentUtil']
    clist = itchat.search_chatrooms(name=u'Connectivity CN')
    olist = clist[0]["UserName"]
    itchat.send(inPercent_dict, olist)

if __name__ == '__main__':
    main()
