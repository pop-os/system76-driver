from system76driver.util import create_support_logs
import shutil
from os import path
import os

(tmp, tgz) = create_support_logs()

print(tgz)
shutil.copy(tgz, os.getcwd())
shutil.rmtree(tmp)
