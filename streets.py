import numpy as np
# import osmnx as ox
from noiseplanet.matcher import matching

track = np.array([[45.7584882 ,  4.83585996],
                  [45.75848068,  4.83586747],
                  [45.75849549,  4.83585205],
                  [45.75849134,  4.83584647],
                  [45.75848135,  4.8358245 ],
                  # ...
                  [45.75846756,  4.83580848],
                  [45.75844998,  4.83580936],
                  [45.7584067 ,  4.83580086],
                  [45.7584067 ,  4.83580086],
                  [45.75839346,  4.83579883]])

graph = matching.model.graph_from_track(track)

track_coor, route_corr, edgeid, stats = matching.match(graph, track, method='hmm')