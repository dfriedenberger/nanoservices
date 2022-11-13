from .pattern import Pattern

class CMS(Pattern):
    
    def get_name(self):
        return "cms"

    def needs_database(self):
        return True