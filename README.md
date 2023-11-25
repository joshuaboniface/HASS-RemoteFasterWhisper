# Remote Faster Whisper for Home Assistant

[Remote Faster Whisper](https://github.com/joshuaboniface/remote-faster-whisper) is a remote but self-hosted Speech-to-Text engine, based off of [Faster Whisper](https://github.com/guillaumekln/faster-whisper). With [Home Assistant](https://www.home-assistant.io/), it allows you to create your own personal self-hosted voice assistant.

This add-on is based on [AlexxIT's Faster Whisper](https://github.com/AlexxIT/FasterWhisper) addon, tweaked to support RFW instead.

It's a custom component because I don't feel like learning how to "properly" package it.

## Installation

[HACS](https://hacs.xyz/) > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `joshuaboniface/HASS-RemoteFasterWhisper`, Category: Integration > Add > wait > Remote Faster Whisper > Install

Or manually copy `remote_faster_whisper` folder from latest release to `/config/custom_components` folder.

## Configuration

Settings > Integrations > Add Integration > Remote Faster Whisper

There are 3 configuration options:

1. The RemoteFasterWhisper base URI. This should be the base URI (without the `/transcribe` endpoint!) of your RemoteFasterWhisper instance.

2. The language of the RemoteFasterWhisper instance. This doesn't actually do anything and defaults to English (`en`), but is here for STT provider compatibility.

3. A boolean to turn on or off Assist Pipeline name prefixing. See below.

## Pipeline Name Prefixing

This functionality requires a HomeAssistant version which includes [PR #104523](https://github.com/home-assistant/core/pull/104523).

This feature allows the prefixing of text returned by RemoteFasterWhisper with the name of the Assist pipeline that called it.

This can be used to build a series of Assist Pipelines which will match entities with a given prefix.

### An example: my own HomeAssistant setup

I have two rooms/areas, "Garage" and "Bedroom". Both have a Voice Assistant satellite, and both have a series of entities which overlap, for example "heater".

In HomeAssistant, these entries are called, respectively, "Garage heater" and "Bedroom heater".

Without this option enabled, commands to either satellite must include the room name as well, which results in longer voice commands and more possibility for error in the STT engine.

With this option enabled, however, one could then create two assist pipelines, named "Garage" and "Bedroom", then assign the Voice Assistant satellite for each room to its respective pipeline.

The pipeline name will then be pre-pended automatically to the text returned by RemoteFasterWhisper, allowing one to simply say "heater" in each location, which is then returned to the Assist pipeline as "Garage heater" or "Bedroom heater", respectively.
