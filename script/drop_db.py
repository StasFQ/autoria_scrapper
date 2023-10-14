import subprocess
import shutil
import os
import datetime

from utils.celery_config import app


@app.task
def dumper():
    db_user = 'postgres'
    db_name = 'postgres'
    dump_file = f'dump_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.sql'
    dump_folder = 'dumps/'

    subprocess.run(['pg_dump', '-U', db_user, db_name, '-f', dump_file])

    if not os.path.exists(dump_folder):
        os.makedirs(dump_folder)
    shutil.move(dump_file, os.path.join(dump_folder, dump_file))
