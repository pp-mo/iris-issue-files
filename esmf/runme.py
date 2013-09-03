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

    # Plot source cell boundaries
    ax = plt.axes(projection=source_proj)

    part_src = source[-20:-5, -15:]
    src_x_coord = part_src.coord('longitude')
    src_y_coord = part_src.coord('latitude')
    src_x_coord.guess_bounds()
    src_y_coord.guess_bounds()
    src_x_points = np.hstack([src_x_coord.bounds[:,0], src_x_coord.bounds[-1:, 1]])
    src_y_points = np.hstack([src_y_coord.bounds[:,0], src_y_coord.bounds[-1:, 1]])
    for x0, x1 in zip(src_x_points[:-1], src_x_points[1:]):
      for y in src_y_points:
        xx = np.array([x0, x1])
        yy = np.array([y, y])
        plt.plot(xx, yy, linewidth=1.0, color='g')
    for y0, y1 in zip(src_y_points[:-1], src_y_points[1:]):
      for x in src_x_points:
        xx = np.array([x, x])
        yy = np.array([y0, y1])
        plt.plot(xx, yy, linewidth=1.0, color='g')
    xx, yy = np.meshgrid(src_x_points, src_y_points)
    plt.scatter(xx.flat, yy.flat, c='g', marker='o', s=15.0)

    # Plot target (regridded) cell boundaries
    part_tgt = regridded[-10:, -10:]
    tgt_x_coord = part_tgt.coord('grid_longitude')
    tgt_y_coord = part_tgt.coord('grid_latitude')
    tgt_x_coord.guess_bounds()
    tgt_y_coord.guess_bounds()
    tgt_x_points = np.hstack([tgt_x_coord.bounds[:,0], tgt_x_coord.bounds[-1:, 1]])
    tgt_y_points = np.hstack([tgt_y_coord.bounds[:,0], tgt_y_coord.bounds[-1:, 1]])
    for x0, x1 in zip(tgt_x_points[:-1], tgt_x_points[1:]):
      for y in tgt_y_points:
        xx = np.array([x0, x1])
        yy = np.array([y, y])
        plt.plot(xx, yy, linewidth=0.5, color='r', transform=regridded_crs)
    for y0, y1 in zip(tgt_y_points[:-1], tgt_y_points[1:]):
      for x in tgt_x_points:
        xx = np.array([x, x])
        yy = np.array([y0, y1])
        plt.plot(xx, yy, linewidth=0.5, color='r', transform=regridded_crs)
    xx, yy = np.meshgrid(tgt_x_points, tgt_y_points)
    plt.scatter(xx.flat, yy.flat, marker='o', color='r', s=15.0, transform=regridded_crs)

    # Plot the masked points in the source projection
    for ndi in masked:
        print "index", ndi
        
        regridded_x = regridded.coord(axis='x').points[ndi[1]]
        regridded_y = regridded.coord(axis='y').points[ndi[0]]
        print "    regridded_x {}, regridded_y {}".format(regridded_x, regridded_y)
        
        source_x, source_y = source_crs.transform_point(regridded_x, regridded_y, regridded_crs)
        print "    source_x {}, source_y {}".format(source_x, source_y)

        plt.scatter([source_x], [source_y], c='r', marker='x', s=125.0, linewidth=5.0)

    ax.coastlines("10m")
    ax.set_extent([16, 18, 62, 63.5])
    plt.savefig('figure_1.png')
    
    
