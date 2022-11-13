import abc


class Pattern(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def get_name(self):
        """Returns the name of the pattern"""
        return

    @abc.abstractmethod
    def needs_database(self):
        """Returns if pattern requires database"""
        return
