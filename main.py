from activities import *

def main():
    activity = LVMActivity("https://www.lasvegasmarket.com/Market%20Map/")

    #activity = CustServicePortal("https://customaticparts.com/servicePortal/")

    #activity = HPMActivity("https://www.highpointmarket.org/exhibitor")
    activity.start_driver()


if __name__ == '__main__':
    main()
