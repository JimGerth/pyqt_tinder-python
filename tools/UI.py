
class UI: # interface for all UI classes that are compatible with this program

    def show_image(self, image, cmap, interpolation):
        raise NotImplementedError

    def connect_single_classification_listener(self):
        raise NotImplementedError

    def connect_multi_classification_listener(self):
        raise NotImplementedError

    def connect_skip_classification_listener(self):
        raise NotImplementedError