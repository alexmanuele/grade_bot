import pkgutil
import sys
def main():
    if(pkgutil.find_loader("selenium")):
        print(0)
        sys.exit(0)
    print(1)
    sys.exit(1)


if __name__ == "__main__":
    main()
