from .pattern import Pattern

class Repository(Pattern):
    
    def get_name(self):
        return "repository"

    def needs_database(self):
        return True