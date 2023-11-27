# Remote Faster Whisper for Home Assistant

[Remote Faster Whisper](https://github.com/joshuaboniface/remote-faster-whisper) is a remote but self-hosted Speech-to-Text engine, based off of [Faster Whisper](https://github.com/guillaumekln/faster-whisper). With [Home Assistant](https://www.home-assistant.io/), it allows you to create your own personal self-hosted voice assistant.

This add-on is based on [AlexxIT's Faster Whisper](https://github.com/AlexxIT/FasterWhisper) addon, tweaked to support RFW instead.

It's a custom component because I don't feel like learning how to "properly" package it.

## Installation

[HACS](https://hacs.xyz/) > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `joshuaboniface/HASS-Remote Faster Whisper`, Category: Integration > Add > wait > Remote Faster Whisper > Install

Or manually copy `remote_faster_whisper` folder from latest release to `/config/custom_components` folder.

## Configuration

Settings > Integrations > Add Integration > Remote Faster Whisper

There are 3 configuration options:

1. The Remote Faster Whisper base URI. This should be the base URI (without the `/transcribe` endpoint!) of your Remote Faster Whisper instance.

2. The language of the Remote Faster Whisper instance. This doesn't actually do anything and defaults to English (`en`), but is here for STT provider compatibility.

3. A "Result Prefix" string to prepend to any returned text.

## Result Prefixing

This feature allows the prefixing of text returned by Remote Faster Whisper with some arbitrary text, for instance the name of a room or location in HomeAssistant.

This can be used to build a series of STT providers and Assist pipelines which will match entities with a given prefix.

### An example: my own HomeAssistant setup

I have two rooms/areas, "Garage" and "Bedroom". Both have a Voice Assistant satellite, and both have a series of entities which overlap, for example "heater".

In HomeAssistant, these entries are called, respectively, "Garage heater" and "Bedroom heater".

Without this ability, commands to either satellite must include the room name as well, which results in longer and more cumbersome voice commands and more possibility for error in the STT engine.

With this ability, however, one could then:

* Create two Remote Faster Whisper STT provider instances, with the "Result Prefix"es of "Garage" and "Bedroom" respectively.

* Create two separate Assist pipelines, one for each location, with the STT provider set to the corresponding "Garage" and "Bedroom" STT providers.

* Assign the Voice Assistant satellite for each room to its respective pipeline.

This would thus enable room-specific results, for instance in the Garage, speaking "heater on" would translate to "Garage heater on", thus matching the "Garage heater" entity without ever needing to say the word "Garage".

### Caveats

The major caveats of this approach are:

* All entities must named accordingly. For example, if your entity is in the "Bedroom" zone, it **must** start with the word "Bedroom" or it will not match.

* You cannot control entities outside of the zone with the sattelite, as the entity will be prepended unconditionally. For example, trying to control the "Garage heater" from the "Bedroom" voice satellite/pipeline is impossible.

Future versions may attempt to work around these issues intelligently.
