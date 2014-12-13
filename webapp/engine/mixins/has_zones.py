"""
This module exports the HasZones mixin.
"""


class HasZones(object):

    """
    A class that inherits from this class has zones. This mixin provides
    the add_zones and add_zone functions.
    """

    def __init__(self):
        super(HasZones, self).__init__()

        self.zones = {}

    def add_zones(self, zone_list):
        """
        This is mainly a utility function. It takes in a list of zone
        configuratons that should be added and calls add_zone for each.
        """

        for zone in zone_list:
            self.add_zone(zone)

    def add_zone(self, zone_config):
        """
        Adds a zone to the current object. The zone_config should be a dictonary
        with the following keys:

            * name: The name of the zone. This means you will be able to aacess
              the zone via self.{name}
            * multiplicity (optional): If this is specified this determines how
              many copies of this zone should be added. Each zone will be given
              the name self.{base_name}{number} with the number being 0 indexed.
              For example, if multiplicity is 2 and name is foo then we will
              create zones foo0 and foo1.
        All other keys are passed through to the zone configuration.
        """

        multiplicity = zone_config.get('multiplicity', None)
        name = zone_config['name']
        if multiplicity is not None:
            multiplicity = int(multiplicity)
            for i in range(multiplicity):
                self.add_zone_internal(name + str(i), zone_config)
        else:
            self.add_zone_internal(name, zone_config)

    def add_zone_internal(self, name, zone_config):
        """
        An internal function for adding a zone. Generally, calls should go
        through the add_zone. This allows an explicitly specified name to
        work around some complications with multiplicity.
        """

        from engine.core.zone import Zone

        zone_object = Zone()
        zone_object.name = name
        zone_object.load_config(zone_config, ignore_keys=['name',
                                                          'multiplicity'])
        self.zones[name] = zone_object
        setattr(self, name, zone_object)
        self.add_zone_callback(zone_object)

    def add_zone_callback(self, new_zone):
        """
        This callback can be overriden by subclasses that might want to perform
        some action when a zone is added.
        """

        pass
