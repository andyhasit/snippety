
class MarkerSelector:
    """Selects the type of Marker to provide based in the string.
    Exists as a separate class for dependency injection.
    """
    def get_marker(self, marker_text, marker_sequence):
        if marker_text.find('*') > 0:
            return IteratorMarker(marker_text, marker_sequence)
        else:
            return StandardMarker(marker_text, marker_sequence)

