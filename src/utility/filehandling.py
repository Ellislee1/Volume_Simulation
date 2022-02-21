#!/usr/bin/env python
"""A collection of methods used for handling files.

load_json: loads a JSON file and auto preps it
prep_routes: Prepares routes adding them to the route object.
prep_wpts: Prepares waypoint by adding them to the waypoint object
"""

import json
import string

from src.geography.route import Route
from src.geography.waypoint import Waypoint

__author__ = "Ellis Thompson"
__credits__ = ["Ellis Thompson"]

__license__ = "GNU GPLv3"
__maintainer__ = "Ellis Thompson"
__email__ = "thompson_e@gwu.edu"
__status__ = "Development"


def load_json(path: string) -> (dict, dict):
    """
    Load a JSON file and prep the data from that file

    Parameters
    ----------
    path: string
        The path to the JSON file
    """
    f = open(path)

    data = json.load(f)

    waypoints = {}

    for wpt in data['waypoints']:
        w = Waypoint(wpt['_id'], wpt['x'], wpt['y'])
        waypoints[w._id] = w
    
    routes = {}
    for rte in data['routes']:
        route = []
        for wpt in rte['route']:
            route.append(waypoints[wpt])
        r = Route(rte['_id'], route)
        routes[r._id] = r
    
    return waypoints, routes
