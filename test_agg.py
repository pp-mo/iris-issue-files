
import numpy

import iris
import iris.cube
import iris.analysis
from iris.coords import DimCoord


cube = iris.cube.Cube(numpy.ones((3,3,3,3)), long_name="original_cube")

cube.add_dim_coord(DimCoord([1,2,3], long_name="x"), 3)
cube.add_dim_coord(DimCoord([1,2,3], long_name="y"), 2)
cube.add_dim_coord(DimCoord([1,2,3], long_name="z"), 1)
cube.add_dim_coord(DimCoord([1,2,3], long_name="w"), 0)

print "------------------"
print cube

mean = cube.aggregated_by("w", iris.analysis.MEAN)
mean.long_name = "aggregated_cube"
print "------------------"
print mean
