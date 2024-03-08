from libs.libs import (
    datetime,
    configparser,
    os,
    shutil,
    json,
    time,
    logging,
    init,
    AnsiToWin32,
    Fore,
    sys,
)

#! utility function

config = configparser.ConfigParser()
config.read("./config.ini")

# custom cmd color
init(autoreset=True)
stream = AnsiToWin32(sys.stderr).stream


def cmd_printer(type: str, msg: str):
    if type == "WARNING":
        print(Fore.YELLOW + msg, file=stream)
    elif type == "ERROR":
        print(Fore.RED + msg, file=stream)
    elif type == "SUCCESS":
        print(Fore.GREEN + msg, file=stream)
    elif type == "INFO":
        print(Fore.BLUE + msg, file=stream)


def get_current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def format_current_time():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H-%M-%S")
    return formatted_time


def create_daily_folders():
    path = config["PATH"]["IMAGE_NG_FOLDER"]
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join(path, current_date)
    os.makedirs(folder_path, exist_ok=True)


def handle_remove_old_folders():
    folder_to_keep = int(config["SETTING"]["FOLDER_TO_KEEP"])
    path = config["PATH"]["IMAGE_NG_FOLDER"]
    subfolders = [f.path for f in os.scandir(path) if f.is_dir()]
    subfolders.sort()
    if len(subfolders) > folder_to_keep:
        folders_to_delete = subfolders[: len(subfolders) - folder_to_keep]
        for folder_to_delete in folders_to_delete:
            try:
                shutil.rmtree(folder_to_delete)
                print(f"Removed old folder: {folder_to_delete}")
            except Exception as e:
                cmd_printer("ERROR", f"Remove error '{folder_to_delete}': {e}")


def setup_logger():
    path_dir_log = "./logs/"
    time_day = time.strftime("%Y_%m_%d")
    logger = logging.getLogger("MyLogger")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler(f"{path_dir_log}{time_day}.log")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    return logger


def read_config(self):
    self.COM_PLC = config["PLC"]["COM"]
    self.BAUDRATE_PLC = config["PLC"]["BAUDRATE"]
    self.ID_C1 = int(config["CAMERA"]["IDC1"])
    self.SCAN_LIMIT = int(config["SETTING"]["SCAN_LIMIT"])
    self.NUM_CAMERA = int(config["SETTING"]["NUM_CAMERA"])
    self.IS_SAVE_NG_IMAGE = int(config["SETTING"]["IS_SAVE_NG_IMAGE"])
    self.IS_OPEN_CAM_PROPS = int(config["SETTING"]["IS_OPEN_CAM_PROPS"])

    self.MIN_THRESH = int(config["THRESH"]["MIN_THRESH"])
    self.MAX_THRESH = int(config["THRESH"]["MAX_THRESH"])
    self.THRESH_JUMP = int(config["THRESH"]["THRESH_JUMP"])

    self.TIME_SLEEP = float(config["MES"]["TIME_SLEEP"])
    self.MAX_WAIT = float(config["MES"]["MAX_WAIT"])
    self.MES_APP_NAME = config["MES"]["MES_APP_NAME"]
    self.MES_PACKING_QTY_ID = config["MES"]["MES_PACKING_QTY_ID"]
    self.MES_BACKEND = config["MES"]["BACKEND"]


handle_remove_old_folders()
create_daily_folders()
logger = setup_logger()
