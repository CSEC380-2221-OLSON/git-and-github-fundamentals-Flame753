import sys

class Scraper:
     pass

def get_command_args():
    if (len(sys.argv)-1) < 3:
        # Stopping the script before breaking something
        sys.exit()
    # Assuming the first 3 inputs was enter correctly. NO sanitaion was done! 
    return sys.argv[1:4]


if __name__ == "__main__":
    domain, url, depth= get_command_args()
    print(domain, url, depth)