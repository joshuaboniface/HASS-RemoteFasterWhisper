import asyncio
import logging

import struct

from re import sub

from requests import post as requests_post
from collections.abc import AsyncIterable

from homeassistant.components import stt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([RemoteFasterWhisperSTT(hass, config_entry)])


class RemoteFasterWhisperSTT(stt.SpeechToTextEntity):
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        self.config: ConfigEntry = config_entry
        self.uri: str = config_entry.data["uri"]
        self.language: str = config_entry.data["language"]
        self.result_prefix: str = config_entry.data["result_prefix"]
        
        if self.result_prefix:
            unique_id_prefix = "_" + sub(r"[',\. ]". "_", self.result_prefix)
        else:
            unique_id_prefix = ""

        self.hass = hass

        self._attr_name = f"Remote Faster Whisper"
        self._attr_unique_id = f"{config_entry.entry_id[:7]}{unique_id_prefix}-stt}"

    @property
    def supported_languages(self) -> list[str]:
        return [self.language]

    @property
    def supported_formats(self) -> list[stt.AudioFormats]:
        return [stt.AudioFormats.WAV]

    @property
    def supported_codecs(self) -> list[stt.AudioCodecs]:
        return [stt.AudioCodecs.PCM]

    @property
    def supported_bit_rates(self) -> list[stt.AudioBitRates]:
        return [stt.AudioBitRates.BITRATE_16]

    @property
    def supported_sample_rates(self) -> list[stt.AudioSampleRates]:
        return [stt.AudioSampleRates.SAMPLERATE_16000]

    @property
    def supported_channels(self) -> list[stt.AudioChannels]:
        return [stt.AudioChannels.CHANNEL_MONO]

    def getTranscription(self, _bytes, metadata):
        _LOGGER.info(metadata)

        # Convert the "audio" bytestring to WAV
        # Courtesy of UllcSahin on SO: https://stackoverflow.com/a/66367870/5253131
        _nchannels = int(metadata.channel)
        _framerate = int(metadata.sample_rate)
        _sampwidth = 2 # This is a magic number; I don't know why 2 worked or where
                       # to get that from the metadata, but ¯\_(ツ)_/¯

        WAVE_FORMAT_PCM = 0x0001
        initlength = len(_bytes)
        bytes_to_add = b'RIFF'

        _nframes = initlength // (_nchannels * _sampwidth)
        _datalength = _nframes * _nchannels * _sampwidth

        bytes_to_add += struct.pack('<L4s4sLHHLLHH4s',
            36 + _datalength, b'WAVE', b'fmt ', 16,
            WAVE_FORMAT_PCM, _nchannels, _framerate,
            _nchannels * _framerate * _sampwidth,
            _nchannels * _sampwidth,
            _sampwidth * 8, b'data')

        bytes_to_add += struct.pack('<L', _datalength)
        audio = bytes_to_add + _bytes

        # Hit the RFW API
        ret = requests_post(f"{self.uri}/transcribe", files={"audio_file": audio})
        _LOGGER.info(ret)
        jret = ret.json()
        _LOGGER.info(jret)
        return jret

    async def async_process_audio_stream(
        self, metadata: stt.SpeechMetadata, stream: AsyncIterable[bytes]
    ) -> stt.SpeechResult:
        _LOGGER.info(f"process_audio_stream start, config: {self.config.data}")

        audio = b""
        async for chunk in stream:
            audio += chunk

        _LOGGER.info(f"process_audio_stream transcribe: {len(audio)} bytes")

        try:
            jret = await self.hass.async_add_executor_job(self.getTranscription, audio, metadata)
            _LOGGER.info(jret)
        except Exception as e:
            _LOGGER.error(f"failed to transcribe: {e}")
            return stt.SpeechResult("", stt.SpeechResultState.ERROR)

        text = jret.get("text")

        if self.result_prefix:
            text = f"{self.result_prefix} {text}"

        _LOGGER.info(f"process_audio_stream end: {text}")

        return stt.SpeechResult(text, stt.SpeechResultState.SUCCESS)
