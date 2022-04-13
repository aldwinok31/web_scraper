from activities import *

def main():
    #activity = LVMActivity("https://www.lasvegasmarket.com/Market%20Map/")
    #activity.start_driver()

    activity = CustServicePortal("http://localhost:8080/troubleshoot/")
    activity.start_driver()


if __name__ == '__main__':
    main()
