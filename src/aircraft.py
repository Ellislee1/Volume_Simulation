class Aircraft:
    """
    Defines an aircraft and its calculations to take each step

    Attributes
    ----------
    _id: string
        The given ID of the aircraft
    pos: point
        The position of the aircraft
    spd: float
        The speed of the aircraft
    alt: float
        The altitude of the aircraft
    heading: float
        The heading of the aircraft
    scale:
        The distance scale of the environment
    route: Route
        The route of the aircraft

    Methods
    -------
    """
    def __init__(self, _id:string, start_pos:Point, spd:float = 30, alt:float = 100, heading:float = 0, scale:int = 1, route:Route = None):
        """
        Parameters
        ----------
        _id: string
            The given ID of the aircraft
        start_pos: point
            The starting position of the aircraft
        spd: float
            The starting speed of the aircraft
        alt: float
            The altitude of the aircraft
        heading: float
            The heading of the aircraft
        scale:
            The distance scale of the environment
        route: Route
            The route of the aircraft
        """
        self._id = _id
        self.position = start_pos
        self.spd = spd
        self.alt = alt
        self.heading = heading
        self.scale = scale
        self.route = route 