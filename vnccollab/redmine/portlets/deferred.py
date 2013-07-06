from plone.app.portlets.portlets import base


class DeferredRenderer(base.DeferredRenderer):
    '''VNC own version of DeferredRenderer.
    '''

    def update(self):
        self.initializing = True
        self.metadata = self.get_metadata()

    def deferred_update(self):
        self.refresh()
        self.metadata = self.get_metadata()
        self.initializing = False

    def refresh(self):
        raise NotImplemented("You must implement 'refresh' as a method")

    def get_metadata(self):
        # We don't always get the metadata
        if getattr(self, '__portlet_metadata__', False):
            metadata = self.__portlet_metadata__
            return dict(
                manager=metadata['manager'],
                name=metadata['name'],
                key=metadata['key']
            )
        else:
            return dict(manager='', name='', key='')
