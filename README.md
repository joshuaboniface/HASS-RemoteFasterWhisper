# Remote Faster Whisper for Home Assistant

[Remote Faster Whisper](https://github.com/joshuaboniface/remote-faster-whisper) is a remote but self-hosted Speech-to-Text engine, based off of [Faster Whisper](https://github.com/guillaumekln/faster-whisper). With [Home Assistant](https://www.home-assistant.io/), it allows you to create your own personal self-hosted voice assistant.

This add-on is based on [AlexxIT's Faster Whisper](https://github.com/AlexxIT/FasterWhisper) addon, tweaked to support RFW instead.

## Installation

[HACS](https://hacs.xyz/) > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `joshuaboniface/HASS-RemoteFasterWhisper`, Category: Integration > Add > wait > Remote Faster Whisper > Install

Or manually copy `remote_faster_whisper` folder from latest release to `/config/custom_components` folder.

## Configuration

Settings > Integrations > Add Integration > Remote Faster Whisper

There are 3 configuration options:

1. The Remote Faster Whisper base URI. This should be the base URI (without the `/transcribe` endpoint!) of your Remote Faster Whisper instance.

2. The language of the Remote Faster Whisper instance. This doesn't actually do anything and defaults to English (`en`), but is here for STT provider compatibility.

3. An optional response prefix. This string will be prepended (along with a `:`) to all results, allowing for more advanced multi-room usage - see below.

## Multiple Instances and Response Prefixes

This solution was borne out of an issue I ran into when using HomeAssistant Assist pipelines with multiple rooms.

Consider for instance, two rooms: Joshua's Bedroom and Basement. Both have their own unique set of lights, etc., but what if you wanted to have a command "all lights off" for both places? Or a fan named "overhead fan" in both places?

HomeAssistant Assist does not, at least as of late-2024, support this natively, at least as far as I can tell, without resorting to cumbersome voice phrases like "joshua's bedroom overhead fan off". If you don't, you'll get a conflict and possibly leave one room "in the dark" unintentionally, or get no response at all because HomeAssistant couldn't determine which entity you actually meant. This bothered me, and after a suggestion within the Assist codebase to "fix" it was rejected, I built it into this stage of the pipeline instead.

HASS-RFW works around this by supporting multiple instances and response prefixes. For example, in my HASS I have 4 zones with voice satellites, and thus 4 discrete instances of this component with unique prefixes, like so:

![Components](/images/components.png)

Each of those instances has a different response prefix, corresponding to the room the satellite is in.

I then have multiple Assist pipelines, similarly one for each location, which use their corresponding HASS-RFW component.

![Pipelines](/images/pipelines.png)

Finally, individual exposed entities in each area have aliases added with the prefix, which enables delineation based on the area.

![Entities](/images/entities.png)

This allows for a seamless, powerful restriction of commands to various areas, as well as the ability for a device with the same name to coexist in multiple areas. For example, I can have a fan called "overhead fan" in both my Garage zone and my Joshua's Bedroom zone, and if I say "overhead fan on" in my garage, it will trigger the correct fan, without any conflicts or misunderstandings on Home Assistant's part.
