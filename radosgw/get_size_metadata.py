import argparse
import requests #needs to be installed
import json

parser = argparse.ArgumentParser(description='Get data of your project from your object storage service.')
parser.add_argument('--user', type=str, required=True, help='Portal customer account')
parser.add_argument('--password', type=str, required=True, help='Portal customer password')
parser.add_argument('--project', type=str, required=True, help='Portal customer project ID. \n '
                                                               'You can found your project ID in \n'
                                                               'https://acloud.ormuco.com/#/api_docs')
args = parser.parse_args()

auth_payload = {
      "auth": {
          "identity": {
              "methods": [
                  "password"
              ],
              "password": {
                  "user": {
                      "name": args.user,
                      "password": args.password
                  }
              }
          },
          "scope": {
              "project": {
                  "id": args.project
              }
          }
      }
    }


def get_auth():
    token_url = 'localhost:5000/v3/auth/tokens'
    payload = json.dumps(auth_payload)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    res = requests.post(token_url, data=payload, headers=headers)
    print(res.json())
    return res

def get_swift_auth(authentication):
    url = "localhost:6780/swift/v1"
    # headers = {"X-Auth-Token": authentication["token"]["id"]}
    headers = {"X-Auth-Token": authentication["token"]["id"]}
    return url, headers

def get_quota(authentication):
    url='localhost:6780/auth'
    headers={'X-Auth-User': 'admin-api-user:swift', 'X-Auth-Key': 'barSecretKey'}
    print(url)
    res = requests.get(url, headers=headers)
    print("1.", res.headers)
    print("2.", res)
    return res

# def get_containers(authentication):
#     url, headers = get_swift_auth(authentication)
#     res = requests.get(url+args.project+"?format=json", headers=headers)
#     print(res.headers)
#     return res

def get_containers(authentication):
    url, headers = get_swift_auth(authentication)
    res = requests.head(url+args.project+"?format=json", headers=headers)
    print(res.headers)
    return res


def print_data(total_objects, total_bytes):
    print("Total of GB and Objects used in project " + args.project)
    print(round(int(total_bytes) / 1073741824),
          "GB of ", int(107374182400 / 1048576), "GB (",
          round(100.00 - (float(total_bytes) / 1073741824 / int(107374182400 / 1048576)) * 100, 2), "% Free)")
    print(round(int(total_objects)),
          "objects of ", 100000, "Objects (",
          round(100.00 - float(total_objects) / 100000 * 100, 2), "% Free)")


def main():
    authentication_token=get_auth().json()
    stats=get_containers(authentication_token).headers
    # stats2=get_quota(authentication_token)
    print('stat', stats)
    # total_bytes=stats['x-account-bytes-used']
    # total_objects=stats['x-account-object-count']
    # print_data(total_objects, total_bytes)


if __name__ == "__main__":
    main()
