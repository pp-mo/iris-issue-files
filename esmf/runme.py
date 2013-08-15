import iris
from iris.experimental.regrid_conservative import regrid_conservative_via_esmpy
import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":

    source = iris.load_cube("pp_unrot.pp")
    target = iris.load_cube("pp_rotgrid.pp")
    regridded = regrid_conservative_via_esmpy(source, target)

    regridded_crs = regridded.coord(axis='x').coord_system.as_cartopy_crs()
    source_crs = source.coord(axis='x').coord_system.as_cartopy_crs()
    source_proj = source.coord(axis='x').coord_system.as_cartopy_projection()

    # Which data got masked?
    masked = []
    for ndi in np.ndindex(*regridded.data.shape):
        if regridded.data.mask[ndi]:
            masked.append(ndi)
    print "regridded.shape", regridded.shape
    print "masked items at", masked

    # Plot the source
    ax = plt.axes(projection=source_proj)
    xx, yy = np.meshgrid(source.coord(axis='x').points, source.coord(axis='y').points)
    plt.scatter(xx.flat, yy.flat, c='g')
    
    # Plot the masked point in the source projection
    for ndi in masked:
        print "index", ndi
        
        regridded_x = regridded.coord(axis='x').points[ndi[1]]
        regridded_y = regridded.coord(axis='y').points[ndi[0]]
        print "    regridded_x {}, regridded_y {}".format(regridded_x, regridded_y)
        
        source_x, source_y = source_crs.transform_point(regridded_x, regridded_y, regridded_crs)
        print "    source_x {}, source_y {}".format(source_x, source_y)

        plt.scatter([source_x], [source_y], c='r')

    ax.coastlines("10m")
    ax.set_extent([15, 19, 61, 65])
    plt.show()
    
    
