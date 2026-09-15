import sys
from pathlib import Path


def main():

    if getattr(sys, "frozen", False):
        ROOT = Path(sys._MEIPASS)
    else:
        ROOT = Path(__file__).resolve().parent

    app = ROOT / "app.py"

    from streamlit.web import cli as stcli

    sys.argv = [
        "streamlit",
        "run",
        str(app),

        "--server.address=127.0.0.1",
        "--server.headless=true",
        "--browser.serverAddress=127.0.0.1"
    ]

    stcli.main()


if __name__ == "__main__":
    main()