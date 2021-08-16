import requests
import time
import sys
from urllib.parse import urlsplit


def cors_tester(url):
    # Define Testing Origins and Headers
    origin_list = ["*","null","true",".example.foo","_.example.foo","http://example.foo"]
    headers_list = ["Access-Control-Allow-Origin","Access-Control-Allow-Credentials"]
    vulnerability_list = []

    # Send First Request to Determine Vulnerablity...
    print("\nTesting Default",end="\r")
    r1 = requests.get(url)
    for header in headers_list:
        if header in r1.headers:
                if r.headers[header] in origin_list:
                    # print("     DETECTED:",header,":",r1.headers[header],"\n")
                    vulnerability_list.append(f"{header}: {r1.headers[header]}")
    
    # Expanding Test y your url
    expanded_list = origin_list.copy()
    for origin in origin_list:
        split_url = urlsplit(r1.url)
        default_origin = split_url.scheme + "://" + split_url.netloc
        expanded_list.append(default_origin + "." + origin)

    # Testing Different Origins to Make Sure!
    for origin in expanded_list:
        print("Testing","Origin:",origin,end="\r")
        time.sleep(0.25)
        r = requests.get(url,headers={"Origin":origin})
        for header in headers_list:
            if header in r.headers:
                if r.headers[header] in origin_list:
                    # print("     DETECTED:",header,": ",r.headers[header],"\n")
                    vulnerability_list.append(f"{header}: {r.headers[header]}")
    return vulnerability_list

def main(argv):
    try:
        opt,url = argv
        if opt == "-u" or opt == "-U":
            # Add http/https schema if not exist
            if not url.startswith('http://') and not url.startswith('https://'):
                url = "http://" + url
            # Start Test
            r = requests.get(url)
            final_url = r.url
            print(final_url)
            if url != final_url:
                print(f"\nYou have been redirected from {url} to {final_url}")
            time.sleep(0.25)
            vulnerability_list = cors_tester(final_url)
            if len(vulnerability_list):
                print("\n",final_url,"is Vulnerable!\n")
                unique_list = set(vulnerability_list)
                unique_list = list(unique_list)
                for item in unique_list:
                    print(item)
            else:
                print("\n",final_url,"is not Vulnerable...\n")
    except:
        print ('\nError! Something happened...')
        print ('It could be Invalid Input or Connection Problems...')
        print ("(Ex: CORSmap.py -u https://example.com)\n")
        sys.exit(2)


if __name__ == '__main__':
    main(sys.argv[1:])
