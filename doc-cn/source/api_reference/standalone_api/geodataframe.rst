.. _geodataframe:

GeoDataFrame
=========
.. currentmodule:: arctern

GeoDataFrame inherits pandas DataFrame. It is a DataFrame to store and process geometric data.

Constructor
-----------
.. autosummary::
   :toctree: api/
   :template: autosummaryclass.rst

   GeoDataFrame

GeoDataFrame Functions
---------------------
.. autosummary::
   :toctree: api/

    GeoDataFrame.to_geopandas
    GeoDataFrame.from_geopandas
    GeoDataFrame.to_json
    GeoDataFrame.from_file
    GeoDataFrame.to_file
    GeoDataFrame.crs
    GeoDataFrame.set_geometry
    GeoDataFrame.dissolve
    GeoDataFrame.merge
