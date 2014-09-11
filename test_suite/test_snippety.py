from snippety import *
from snippety.test_suite import TestBase

import os
import shutil
from tempfile import mkdtemp

class TestSnippety(TestBase):



    def test_basic(self):
        def full_names(file_sets):
            """Gets full file paths from files in file_sets and sorts them."""
            files = []
            for file_set in file_sets:
                files.extend([os.path.join(tmp_dir, f) for f in file_set])
            files.sort()
            return files

        py_files = ['f1.py', 'f2.py']
        py_files_under_git = ['.git\\old78f1.py', '.git\\fadad2.py']
        py_files_under_test = ['test\\test_f1.py', 'test\\test_f2.py']
        pyc_files = ['f1.pyc', 'f2.pyc']
        pyc_files_under_git = ['.git\\old78f1.pyc', '.git\\fadad2.pyc']
        pyc_files_under_test = ['test\\test_f1.pyc', 'test\\test_f2.pyc']

        all_file_sets = [
            py_files,
            py_files_under_git,
            py_files_under_test,
            pyc_files,
            pyc_files_under_git,
            pyc_files_under_test,
            ]

        tmp_dir = mkdtemp()
        for file_set in all_file_sets:
            for file_name in file_set:
                target = os.path.join(tmp_dir, file_name)
                if not os.path.exists(os.path.dirname(target)):
                    os.makedirs(os.path.dirname(target))
                f = open(target, 'w+')

                f.close()

        sn = Snippety()

        found = sn.collect_files(tmp_dir)
        assert found == full_names(all_file_sets)

        found = sn.collect_files(tmp_dir, include=['*'])
        assert found == full_names(all_file_sets)

        # Only search for one file type
        found = sn.collect_files(tmp_dir, include=['*.py'])
        assert found == full_names([py_files, py_files_under_test, py_files_under_git])

        # Only search in one directory
        found = sn.collect_files(tmp_dir, include=['.git\\*'])
        assert found == full_names([py_files_under_git, pyc_files_under_git])

        # exlude a file type
        found = sn.collect_files(tmp_dir, exclude=['*.pyc*'])
        assert found == full_names([py_files, py_files_under_test, py_files_under_git,])

        # exlude a subdirectory
        found = sn.collect_files(tmp_dir, exclude=['.git\\*'])
        assert found == full_names([py_files, py_files_under_test, pyc_files, pyc_files_under_test])

        # combine include and exclude
        found = sn.collect_files(tmp_dir, include=['*.py'], exclude=['.git\\*'])
        assert found == full_names([py_files, py_files_under_test])

        shutil.rmtree(tmp_dir)



if __name__ == "__main__":
    import pytest
    pytest.main()