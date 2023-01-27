from pathlib import Path

pth_pwd = Path(__file__).resolve().parent
pth_appRoot = pth_pwd.parent

pth_root = str(pth_appRoot) + "/"
pth_api = pth_root + "api/"
pth_data = pth_root + "data/"
pth_lib = pth_root + "lib/"
pth_model = pth_root + "model/"
pth_qa = pth_root + "qa/"
pth_routes = pth_root + "routes/"
pth_templ = pth_root + "templ/"
pth_uix = pth_root + "uix/"
