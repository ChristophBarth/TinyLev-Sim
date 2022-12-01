class Plot_Data:
    def __init__(self, data, cmap, vmin=None, vmax=None, desc="", xlabel="", ylabel=""):
        self.data = data
        self.cmap = cmap
        self.vmin = vmin
        self.vmax = vmax
        self.desc = desc
        self.xlabel = xlabel
        self.ylabel = ylabel
