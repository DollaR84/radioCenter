from concurrent.futures import ThreadPoolExecutor, Future
import os
import re
import requests
from threading import Event
from typing import Optional

import addonHandler
from gui.message import displayDialogAsModal
from logHandler import log

import wx

from .. import vlc


addonHandler.initTranslation()


class RadioRecorder:

    def __init__(self, parent, record_path: str, stream_url: str):
        self.parent = parent
        self.record_path: str = record_path
        self.stream_url: str = stream_url
        self.data: dict = {}

        self.file_name: str = None
        self.ext: str = '.mp3'
        self.is_progress_recording: bool = True

        self.stop_event: Event = Event()
        self._executor: ThreadPoolExecutor = ThreadPoolExecutor(1)
        self._queuedFuture: Optional[Future] = self._executor.submit(self.record)

    def get_name_file_for_record(self, ext: str = ".mp3") -> str:
        names = set(x[:-4] for x in os.listdir(self.record_path) if x.endswith(ext))

        label = self.get_audio_label()
        if label and label not in names:
            return os.path.join(self.record_path, "".join([label, ext]))

        else:
            for i in range(10**8):
                if label:
                    filename = " ".join([label, "%08i" % i])
                else:
                    filename = "%08i" % i

                if filename not in names:
                    return os.path.join(self.record_path, "".join([filename, ext]))

    def get_file_name(self):
        self.data = self.parent.radio.data

        if 'aac' in self.stream_url:
            self.ext = ".aac"
        return self.get_name_file_for_record(self.ext)

    def get_audio_label(self) -> str | None:
        result = None

        now_playing = self.data.get(vlc.Meta.NowPlaying)
        if now_playing:
            result = now_playing

        album_data = [
            self.data.get(vlc.Meta.AlbumArtist),
            self.data.get(vlc.Meta.Album),
            self.data.get(vlc.Meta.ShowName),
        ]
        album_data = [item for item in album_data if item is not None]
        if album_data:
            result = " - ".join(album_data)

        data = [
            self.data.get(vlc.Meta.Artist),
            self.data.get(vlc.Meta.Genre),
            self.data.get(vlc.Meta.Title),
        ]
        data = [item for item in data if item is not None]
        if data:
            result = " - ".join(data)

        return re.sub(r'[\/:*?"<>|+]', " - ", result) if result else None

    def record(self):
        self.file_name = self.get_file_name()
        try:
            responce = requests.get(self.stream_url, stream=True)
        except Exception as error:
            log.error(error, exc_info=True)
            self.is_progress_recording = False
            return

        with open(self.file_name, 'wb') as file_out:
            for block in responce.iter_content(1024):
                file_out.write(block)
                if self.stop_event.is_set():
                    break

        self._executor.shutdown(wait=False)

    def stop(self):
        self.stop_event.set()

        path_to_save = self.get_path_to_save()
        self.save(path_to_save)

    def get_path_to_save(self) -> str | None:
        if not self.parent:
            return None

        title = _("Select file to save")
        audio_label = _("Audio files")
        all_label = _("All files")
        wildcard = f'{audio_label} (*.mp3;*.aac)|*.mp3;*.aac|' \
            f'{all_label} (*.*)|*.*'

        fd = wx.FileDialog(
            self.parent,
            message=title,
            wildcard=wildcard,
            defaultDir=self.record_path,
            defaultFile=os.path.basename(self.file_name),
            style=wx.FD_SAVE,
        )

        if displayDialogAsModal(fd) != wx.ID_OK:
            return None
        return fd.GetPath()

    def save(self, path_to_save: str | None):
        if not path_to_save:
            return

        if path_to_save == self.file_name:
            return

        os.replace(self.file_name, path_to_save)
