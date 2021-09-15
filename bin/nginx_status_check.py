import requests

if __name__ == '__main__':
    try:

        ## Getting the nginx status
        r = requests.get(url = "http://172.27.45.245:80/test_html.html")
        if r.status_code == "200":
            print("Nginx web app is working")
        else:
            print("Nginx web app is Down")
            print("Need some one to look immidiatly")

