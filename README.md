Scoring System
==============


Modules
-------

services/ - contains the service verifiers
            To run the tests cd to the services dir and run `nosetests tests/`

targets/ - contains json descriptions of the services


Targets Specification
---------------------

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

Service Verifiers
-----------------

Service verifers are modules that represent a particular service on an
arbitrary host. Service modules know how to verify that their service is
running, and in most cases can determine the owner of the team/player.

Place service verifiers in the services/ directory. They should subclass the
Service type (see services/__init__.py). They should implement the
`verify_up()` and `owner` methods.

Service modules are passed a configuration dictionary that will consist of
the settings dict specified in the target's json file, as well as a 'host'
value indicating the host/ip of the target on which the service resides.

TODO: ssh keys for authentication?

