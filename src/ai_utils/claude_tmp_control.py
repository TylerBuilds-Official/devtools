import os
import shutil
from pathlib import Path

class ClaudeTmpControl:
    def __init__(self):
        self._claude_tmp_dir = Path(r"C:\Users\tylere.METALSFAB\Desktop\Dev stuff\CLAUDE_TMP")

        self._ensure_tmp_dir_exists()

    def _ensure_tmp_dir_exists(self):
        if not os.path.exists(self._claude_tmp_dir):
            raise FileNotFoundError(f"Temporary directory '{self._claude_tmp_dir}' does not exist. Please ask the user to create a temp directory and adjust the config path in the MCP server.")


    def _resolve_partial_path(self, path):
        try:
            if path.startswith(str(self._claude_tmp_dir)):
                return path
            else:
                return self._claude_tmp_dir / path
        except Exception as e:
            raise Exception(f"Error resolving path: {e}")

    def get_top_level(self):
        contents = os.listdir(self._claude_tmp_dir)
        return contents

    def get_content_deep(self):
        contents = {}
        for root, dirs, files in os.walk(self._claude_tmp_dir):
            contents[root] = {'dirs': dirs, 'files': files}

        return contents


    def list_dir(self, path):
        if path is None:
            raise ValueError("list_dir requires a path argument.")
        path = self._resolve_partial_path(path)
        if self._claude_tmp_dir not in Path(path).parents:
            raise PermissionError("Path outside of the temporary directory. Please use FileSystem tools to interact outside of the temporary directory.")

        contents = []
        for item in os.listdir(path):
            item_path = Path(path) / item
            if item_path.is_dir():
                contents.append(item_path)
        return contents


    def list_files(self, path):
        if path is None:
            raise ValueError("list_files requires a path argument.")
        path = self._resolve_partial_path(path)
        if self._claude_tmp_dir not in Path(path).parents:
            raise PermissionError("Path outside of the temporary directory. Please use FileSystem tools to interact outside of the temporary directory.")

        contents = []
        for item in os.listdir(path):
            item_path = Path(path) / item
            if item_path.is_file():
                contents.append(item_path)
        return contents


    def get_file_content(self, path):
        if path is None:
            raise ValueError("get_file_content requires a path argument.")
        path = self._resolve_partial_path(path)
        if self._claude_tmp_dir not in Path(path).parents:
            raise PermissionError("Path outside of the temporary directory. Please use FileSystem tools to interact outside of the temporary directory.")

        with open(path, 'r') as file:
            content = file.read()

        return content


    def delete_file(self, path):
        if path is None:
            raise ValueError("delete_file requires a path argument.")
        path = self._resolve_partial_path(path)
        if self._claude_tmp_dir not in Path(path).parents:
            raise PermissionError("Path outside of the temporary directory. Please use FileSystem tools to interact outside of the temporary directory.")

        os.remove(path)
        return path


    def delete_dir(self, path):
        if path is None:
            raise ValueError("delete_dir requires a path argument.")
        path = self._resolve_partial_path(path)
        if self._claude_tmp_dir not in Path(path).parents:
            raise PermissionError("Path outside of the temporary directory. Please use FileSystem tools to interact outside of the temporary directory.")

        shutil.rmtree(path)
        return path