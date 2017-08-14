PostSignal
==========

Opens up a url endpoint to which you can POST json objects. These will then be output as signals.

Properties
----------
- **endpoint**(string): Endpoint at which to accept signals.
- **host**(string): Local IP. Defaults to 127.0.0.1.
- **include_headers**(bool): Whether to include headers on post response
- **port**(int): Port to accept signals on. Defaults to 8182.
- **response_headers**(object): Headers to include on post response

Inputs
------

None

Outputs
-------

Creates a new signal for each successful POST to this block.

Commands
--------
- **post**: Notifies a signal from the block immediately, configured with a dictionary parameter.

Dependencies
------------
