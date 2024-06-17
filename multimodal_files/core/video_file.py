from multimodal_files.dependency_requirements import requires_cv2, requires_numpy
from multimodal_files.core.upload_file import UploadFile

try:
    import cv2
    import numpy as np
except ImportError:
    pass

class VideoFile(UploadFile):
    """
    A class to represent a video file.
    """
    @requires_cv2()
    def from_file(self, path_or_handle: str):
        self._reset_buffer()
        cap = cv2.VideoCapture(path_or_handle)
        while (cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                break
            is_success, buffer = cv2.imencode('.png', frame)
            if is_success:
                self._content_buffer.write(buffer)
        cap.release()
        self._content_buffer.seek(0)

    @requires_cv2()
    @requires_numpy()
    def to_video(self, output_path: str, frame_rate: int = 30):

        self._content_buffer.seek(0)
        frames = []
        while True:
            data = np.frombuffer(self._content_buffer.read(), dtype=np.uint8)
            if len(data) == 0:
                break
            frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
            frames.append(frame)

        height, width, layers = frames[0].shape
        size = (width, height)
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'DIVX'), frame_rate, size)

        for frame in frames:
            out.write(frame)
        out.release()

    @staticmethod
    def _necessary_libs_installed():
        try:
            import cv2
            import numpy as np
            return True
        except ImportError:
            return False

    @staticmethod
    def _get_necessary_libs() -> list:
        return ["cv2", "numpy"]