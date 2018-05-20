
from ant.common.dbapi import *
from ant.common.log import *

from doczone.mod import models
import os

class FSE_CONFIG:
    CACHE_DIR = 'cache'
    STORAGE_DIR = 'fs'
    PROJ_DESC_FILE = 'project_desc.txt'
    DEFAULT_USER = None

class FileStorageEngine(object):
    def __init__(self, root_path, converter):
        self.root_path = root_path
        self.converter = converter

        self._init_workplace()
        self._create_db()

        self.user = FSE_CONFIG.DEFAULT_USER

    def _init_workplace(self):

        if not os.path.exists(self.root_path):
            log_emergency("dir {} not exist".format(self.root_path))

        cache_dir = os.path.join(self.root_path, FSE_CONFIG.CACHE_DIR)
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)

            if not os.path.exists(cache_dir):
                log_emergency("fse create path failed: {}".format(cache_dir))

        fs_dir = os.path.join(self.root_path, FSE_CONFIG.STORAGE_DIR)
        if not os.path.exists(fs_dir):
            os.mkdir(fs_dir)

            if not os.path.exists(fs_dir):
                log_emergency("fse create path failed: {}".format(fs_dir))


    def _create_db(self):

        if not models.Column.create():
            log_emergency("create db fail: Column")

        if not models.Project.create():
            log_emergency("create db fail: Project")

        if not models.File.create():
            log_emergency("create db fail: File")

    def set_user(self, user):
        self.user = user

    def _scan_projects(self, path, col_id):
        
        for subdir in os.listdir(path):
            proj_path = path + subdir
            proj_name = subdir

            proj_desc = ''
            proj_desc_file = os.path.join(proj_path, FSE_CONFIG.PROJ_DESC_FILE
            if os.path.isfile(proj_desc_file)):
                fobj = open(proj_desc_file)
                try:
                    proj_desc = fobj.read()
                finally:
                    fobj.close()
            
            self.create_project(proj_name, proj_desc, col_id)
            log_debug("project {} imported".format(proj_name))
 
    def import_projects(self, path):

        for subdir in os.listdir(path):
            col_id = int(subdir)
            column = models.Column.find_one(col_id=col_id)

            if not column:
                log_error("col id {} not found".format(col_id))

            self._scan_projects(os.path.join(path, subdir), col_id)

    def export_projects(self, path):
        pass

    def create_column(self, name, parent_id):
        pass

    def delete_column(self, id):
        pass

    def create_project(self, title, desc, col_id):

        column = models.Column.find_one(col_id=col_id)
        if not column:
            log_error("col id {} not found".format(col_id))

        # TODO
        pass

    def delete_project(self, proj_id):
        pass

    def add_files(self, path, proj_id):
        pass

    def delete_file(self, fid):
        pass

    def move_column(self, col_id, from_parent, to_parent):
        pass

    def move_project(self, proj_id, from_col_id, to_col_id):
        pass

    def move_file(self, fid, from_proj_id, to_proj_id):
        pass
