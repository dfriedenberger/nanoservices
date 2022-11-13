import abc


class Pattern(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def get_name(self, input):
        """Returns the name of the pattern"""
        return
    
