class SNA_Error(Exception):
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super(SNA_Error, self).__init__(message)
        # Now for your custom code...
        self.errors = errors