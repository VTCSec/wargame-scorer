Scoring System
==============

Scoring system for a wargame (hacking simulation).

Scoring will occur according to a configurable time period, though it should
not occur on the hour exactly, rather it will occur randomly during the hour.

Each service on each target will be verified. Verification consists of
checking if a service is up and determining which player/team owns it. If a
service is not up, no points are allocated for that service.

If a target does not have all of its required services online, then no one
receives points for that target. If all the required services are online,
then whoever owns the optional services gets points for those as well.

This robust scoring system, while somewhat complicated, allows for situations
where players/teams can share control on a box, or a situation where a player
compromises a service but does not root the box (defacing a website for
example).

This scoring system is designed to be run as a daemon on the private network
with the hosts. It provides a simple API so clients (e.g., a scoreboard) can get 
live information about the game.


Targets
-------

Each target will have a set of services required to be up in order to receive
(full?) points. This prevents players from rooting a box and then locking it
down completely. It also simulates the real world where machines have specific
functions that must function.

**Specification**

Targets are specified in JSON and loaded by the scorer.

The json specification contains important metadata that allows the scorer
to operate on the target.

The following metadata is required:

 * `name`: the name of the target (displayed on the scoreboard)
 * `host`: the hostname or ip of the target
 * `services`: a list of service JSON objects that are active on this target

The service JSON struct should contain the following keys:

 * `service`: the name of the service (required)
 * `value`: the point value of this service (required)
 * `optional`: whether the service is an optional service (default: false)

Additionally, some services require additional settings (e.g., port,
SSH keys, text to parse, etc). These options should be included as a JSON
object in the specification with the service name as the key.

 Example:

    {
        "name": "Example Host",
        "host": "10.0.0.3",
        "services": [ {"service": "http", "optional": false, "value": 5} ],
        "http": { "port": 80, "text": "Hello World" }
    }

Service Verifiers
-----------------

Service verifers are modules that represent a particular service on an
arbitrary host. Service modules know how to verify that their service is
running, and in most cases can determine the owner of the team/player.

Some examples of possible service verifiers are:

1. An imap service that logs into an imap server and attempts to retrieve some
   mail
2. An smtp service that logs into an smtp server and attempts to send a mail
3. An http that verifes that an HTTP connection can be made and certain text is
   rendered.
4. An ssh service that verifiers an sshd is running on the host

Place service verifiers in the services/ directory. They should subclass the
Service type (see `services/__init__.py`). They should implement the
`verify_up()` and `owner` methods.

Service modules are passed a configuration dictionary that will consist of
the settings dict specified in the target's json file, as well as a 'host'
value indicating the host/ip of the target on which the service resides.

TODO: ssh keys for authentication?

Modules
-------

`services/` - contains the service verifiers
            To run the tests cd to the services dir and run `nosetests tests/`

`targets/` - contains json descriptions of the services


