.. _geoseries:

GeoSeries
=========
.. currentmodule:: arctern

GeoSeries inherits pandas Series. It is a Series to store and process geometric data, and internally stores geometries as bytes objects.

Constructor
-----------
.. autosummary::
   :toctree: api/
   :template: autosummaryclass.rst

   GeoSeries


Attributes
----------
.. autosummary::
   :toctree: api/

   GeoSeries.is_valid
   GeoSeries.length
   GeoSeries.is_simple
   GeoSeries.area
   GeoSeries.geom_type
   GeoSeries.centroid
   GeoSeries.convex_hull
   GeoSeries.npoints
   GeoSeries.envelope

.. TODO: should we use this title?

Constructing Geometry
---------------------
.. autosummary::
   :toctree: api/

    GeoSeries.point
    GeoSeries.polygon_from_envelope
    GeoSeries.geom_from_geojson
    GeoSeries.as_geojson
    GeoSeries.to_wkt
    GeoSeries.to_wkb
    GeoSeries.to_geopandas

    GeoSeries.from_geopandas

Processing Geometry
-------------------
.. autosummary::
   :toctree: api/

   GeoSeries.buffer
   GeoSeries.precision_reduce
   GeoSeries.intersection
   GeoSeries.make_valid
   GeoSeries.simplify
   GeoSeries.set_crs
   GeoSeries.crs
   GeoSeries.to_crs
   GeoSeries.curve_to_line

Spatial Relationship
--------------------
.. autosummary::
   :toctree: api/

   GeoSeries.geom_equals
   GeoSeries.touches
   GeoSeries.overlaps
   GeoSeries.crosses
   GeoSeries.contains
   GeoSeries.intersects
   GeoSeries.within

Measurement
-----------
.. autosummary::
   :toctree: api/

   GeoSeries.distance_sphere
   GeoSeries.distance
   GeoSeries.hausdorff_distance

Aggregation
-----------
.. autosummary::
   :toctree: api/

   GeoSeries.unary_union
   GeoSeries.envelope_aggr

Pandas Methods
--------------
.. TODO: add describe here
.. autosummary::
   :toctree: api/

   GeoSeries.isna
   GeoSeries.notna
   GeoSeries.fillna
   GeoSeries.equals
