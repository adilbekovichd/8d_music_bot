import io
import logging
import os
import math

from pydub import AudioSegment

logger = logging.getLogger(__name__)


# ==============================
# FFmpeg
# ==============================

FFMPEG_DIR = r"C:\Users\alimo\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0-full_build\bin"

FFMPEG_PATH = os.path.join(FFMPEG_DIR, "ffmpeg.exe")
FFPROBE_PATH = os.path.join(FFMPEG_DIR, "ffprobe.exe")

os.environ["PATH"] += os.pathsep + FFMPEG_DIR

AudioSegment.converter = FFMPEG_PATH
AudioSegment.ffmpeg = FFMPEG_PATH
AudioSegment.ffprobe = FFPROBE_PATH


class AudioProcessingError(Exception):
    pass



# ==============================
# Tez 8D effekt
# ==============================

def _apply_8d_effect(audio, cycle_seconds=8):

    # stereo
    audio = audio.set_channels(2)


    duration = len(audio)


    # chap va o'ng kanal
    left = audio.pan(-0.7)
    right = audio.pan(0.7)


    # asosiy 8D harakat
    result = AudioSegment.empty()


    step = 1000  # 1 sekundlik bo'lak


    for pos in range(0, duration, step):

        chunk = audio[pos:pos+step]


        angle = (pos / (cycle_seconds * 1000)) * 2 * math.pi

        pan_value = math.sin(angle)


        chunk = chunk.pan(pan_value)


        result += chunk



    return result



# ==============================
# Convert
# ==============================

def convert_to_8d(
        input_bytes: bytes,
        input_format=None,
        cycle_seconds=8,
        chunk_ms=25
):

    try:

        logger.info("FFmpeg: %s", FFMPEG_PATH)
        logger.info("FFprobe: %s", FFPROBE_PATH)
        logger.info("Size: %s", len(input_bytes))


        audio = AudioSegment.from_file(
            io.BytesIO(input_bytes)
        )


        logger.info(
            "Audio ochildi: %s ms",
            len(audio)
        )


    except Exception as e:

        logger.exception(
            "Audio ochishda xato"
        )

        raise AudioProcessingError(
            "Audio faylni o'qib bo'lmadi."
        ) from e



    try:

        processed = _apply_8d_effect(
            audio,
            cycle_seconds
        )


        output = io.BytesIO()


        processed.export(
            output,
            format="mp3",
            bitrate="192k"
        )


        output.seek(0)


        logger.info(
            "8D tayyor bo'ldi"
        )


        return output



    except Exception as e:

        logger.exception(
            "8D xatosi"
        )

        raise AudioProcessingError(
            "8D formatga o'tkazishda xatolik."
        ) from e