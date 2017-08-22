PostSignal
==========
DEPRECATED, USE web_hanlder BLOCKS INSTEAD - Opens up a url endpoint to which you can POST json objects. These will then be output as signals.

Properties
----------
- **endpoint**: Endpoint at which to accept signals.
- **host**: Local IP. Defaults to 127.0.0.1.
- **include_headers**: Whether to include headers on post response
- **port**: Port to accept signals on. Defaults to 8182.
- **response_headers**: 

Inputs
------

Outputs
-------
- **default**: A new signal for each successful POST to this block.

Commands
--------
- **post**: Notifies a signal from the block immediately, configured with a dictionary parameter.

