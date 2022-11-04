import socket
import os
import re
import yaml
from pathlib import Path



def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip



def create(file,tempfile,config):
    print("Create",file,"from",tempfile)
    with open(tempfile,'r',encoding="UTF-8") as f_in:
        with open(file,'w',encoding="UTF-8") as f_out:
            for line in f_in.readlines():
                pattern = re.compile(r"{{([a-z-]+)}}")
                m = pattern.search(line)
                if m:
                    line = line.replace(m.group(0),config[m.group(1)])

                f_out.write(line)

with open("credentials.yml") as f:
    config = yaml.safe_load(f)

# Add ip
config["host"] = get_ip()



for tempfile in Path('.').rglob('*.template'):
    file = os.path.splitext(tempfile)[0]
    create(file,tempfile,config)
