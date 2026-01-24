# Block youtube for smart tv
#
# Michael Pilgermann (kichkasch@posteo.de)
# 2025-11-02

import requests
from environs import Env

env = Env()
env.read_env() # read .env file, if it exists
api_key = env("API_KEY")
host = env("IP_FIREWALL")
fake_dns_ip = env("FAKE_DNS_IP")
domains_to_block = env.list("DOMAINS")

if not api_key or not host or not fake_dns_ip:
    exit("Configuration in .env not provided. See readme for details")

def applyDnsResolverChanges():
    endpoint = "/api/v2/services/dns_resolver/apply"
    method = "POST"
    url = "https://" + host + endpoint
    response = requests.request(method, url, headers={"x-api-key": api_key}, verify=False)
    return response.json()

def getDomainOverrides():
    endpoint = "/api/v2/services/dns_resolver/domain_overrides"
    method = "GET"

    url = "https://" + host + endpoint
    response = requests.request(method, url, headers={"x-api-key": api_key}, verify=False)  # verify false because we have self signed SSL certificate
    return response.json()['data']

def addDomainOverride(domain):
    endpoint = "/api/v2/services/dns_resolver/domain_override"
    method = ("POST")
    payload = {
        "domain": domain,
        "ip": fake_dns_ip,
        "descr": "Stop youtube",
        "forward_tls_upstream": "true",
        "tls_hostname": "string"
    }

    url = "https://" + host + endpoint
    response = requests.request(method, url, headers={"x-api-key": api_key, "Content-Type": "application/x-www-form-urlencoded"}, verify=False, params=payload)
    return response.ok

def delDomainOverrideEntry(domain, overrides):
    endpoint = "/api/v2/services/dns_resolver/domain_override"
    method = "DELETE"
    url = "https://" + host + endpoint
    for entry in overrides:
        if entry['domain'] == domain:
            id = entry['id']
            response = requests.request(method, url, headers={"x-api-key": api_key, "Content-Type": "application/x-www-form-urlencoded"}, verify=False, params={'id': id})
            return response.ok
    return False

def delDomainOverride(domain, multiple=False):
    overrides = getDomainOverrides()
    entrySucess = delDomainOverrideEntry(domain, overrides)
    if not multiple:
        return entrySucess
    if not entrySucess:
        return False
    while entrySucess:
        entrySucess = delDomainOverrideEntry(domain, overrides)
    return True

def addAllDomainOverrides():
    for i in domains_to_block:
        print (addDomainOverride(i))
    applyDnsResolverChanges()

def delAllDomainOverrides():
    for i in domains_to_block:
        print (delDomainOverride(i, True))
    applyDnsResolverChanges()

if __name__ == '__main__':
    print (getDomainOverrides())
    #addAllDomainOverrides()
    print (getDomainOverrides())
    delAllDomainOverrides()
    print (getDomainOverrides())

