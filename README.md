# Remote Faster Whisper for Home Assistant

[Remote Faster Whisper](https://github.com/joshuaboniface/remote-faster-whisper) is a remote but self-hosted Speech-to-Text engine, based off of [Faster Whisper](https://github.com/guillaumekln/faster-whisper). With [Home Assistant](https://www.home-assistant.io/), it allows you to create your own personal self-hosted voice assistant.

This add-on is based on [AlexxIT's Faster Whisper](https://github.com/AlexxIT/FasterWhisper) addon, tweaked to support RFW instead.

It's a custom component because I don't feel like learning how to "properly" package it.

## Installation

[HACS](https://hacs.xyz/) > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `joshuaboniface/HASS-RemoteFasterWhisper`, Category: Integration > Add > wait > Remote Faster Whisper > Install

Or manually copy `remote_faster_whisper` folder from latest release to `/config/custom_components` folder.

## Configuration

Settings > Integrations > Add Integration > Remote Faster Whisper

There are 2 configuration options:

1. The Remote Faster Whisper base URI. This should be the base URI (without the `/transcribe` endpoint!) of your Remote Faster Whisper instance.

2. The language of the Remote Faster Whisper instance. This doesn't actually do anything and defaults to English (`en`), but is here for STT provider compatibility.
