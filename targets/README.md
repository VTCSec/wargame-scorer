Targets Specification
=====================

Targets are specified in JSON and loaded by the scorer.

The json specification contains important metadata that allows the scorer
to operate on the target.

The following metadata is required:

 * name: the name of the target (displayed on the scoreboard)
 * host: the hostname or ip of the target
 * services: a list of service names that are active on this target

 Additionally, some services require additional settings (e.g., port
 information, SSH keys, text to parse, etc). These options should be included
 as a JSON object in the specification with the service name as the key.

 Example:

    {
        "name": "Example Host",
        "host": "10.0.0.3",
        "services": [ "http" ],
        "http": { "port": 80, "text": "Hello World" }
    }
