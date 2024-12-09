# main script that starts a server listening on endpoints defined in backend/api.py

from api import api


def main():
    print("hello world!")

    api.run()


if __name__ == "__main__":
    main()