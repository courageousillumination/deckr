These are all things that need to be refactored. This
should happen before any significant code changes work
their way in.

* Steps: Steps should probably get their own class of some kind, and the entire logic with the global state needs to be reworked.
* Split out Game: The class is getting to large, it should be split out into several subclasses.
* Integration tests: We need to add actual integration tests and provide a harness for writing your own integration tests when creating games.
* Javascript clean up. It's still somewhat of a mess, and it needs to be fixed.
