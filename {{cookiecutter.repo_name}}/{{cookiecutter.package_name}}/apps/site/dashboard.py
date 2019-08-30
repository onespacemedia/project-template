from jet.dashboard import modules
from osm_jet.dashboard import Dashboard


class OSMDashboard(Dashboard):
    def init_with_context(self, context):
        '''
            Add dashboard widgets for the site here.

            Any widgets you add under `self.available_children` will be available in the widget selector.
            Any widgets you add under `self.children` will be added to a user's dashboard by default.
        '''

        self.available_children.append(modules.AppList)
        self.available_children.append(modules.ModelList)
        self.available_children.append(modules.RecentActions)
        self.available_children.append(modules.LinkList)
        self.children.append(modules.RecentActions(
            'Recent Actions',
            column=1,
        ))
