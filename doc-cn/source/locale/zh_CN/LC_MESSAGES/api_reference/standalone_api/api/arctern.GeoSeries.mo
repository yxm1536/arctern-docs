��    !      $              ,  6   -  ;   d  E   �  V   �  /   =  7   m  ,   �  E   �  9     ;   R  :   �  :   �  &     M   +  [   y  .   �  :     v   ?  �   �  [   d  �   �  b   D     �  O   �  =   �  U   =	  ?   �	  8   �	  3   
  -   @
  C   n
  (   �
  x  �
  �   T  M   P  t   �  �     J   �  �   �  �   �  r   \  q   �  z   A  �   �  w   j  8   �  V     `   r  *   �  *   �  �   )  �   �  Y   ^  t   �  �   -     �  9   �  �   �  |   �  �     6   �  2     /   D  $   t  9   �   :obj:`make_valid <arctern.GeoSeries.make_valid>`\ \(\) :obj:`point <arctern.GeoSeries.point>`\ \(x\, y\[\, crs\]\) Calculate the point set intersection between each geometry and other. Calculates the minimum 2D Cartesian (planar) distance between each geometry and other. Calculates the points number for each geometry. Check whether each geometry "spatially overlaps" other. Check whether each geometry "touches" other. Check whether each geometry and other(elementwise) "spatially cross". Check whether each geometry contains other (elementwise). Check whether each geometry intersects other (elementwise). Check whether each geometry is "spatially equal" to other. Check whether each geometry is within other (elementwise). Compute the centroid of each geometry. Compute the double-precision minimum bounding box geometry for each geometry. Compute the double-precision minimum bounding box geometry for the union of all geometries. Construct geometries from geopandas GeoSeries. Construct geometry from the GeoJSON representation string. Construct polygon(rectangle) geometries from arr_min_x, arr_min_y, arr_max_x, arr_max_y and special coordinate system. Convert curves in each geometry to approximate linear representation, e.g., CIRCULAR STRING to regular LINESTRING, CURVEPOLYGON to POLYGON, and MULTISURFACE to MULTIPOLYGON. For each geometry, compute the smallest convex geometry that encloses all geometries in it. For each geometry, returns a geometry that represents all points whose distance from this geos is less than or equal to "distance". For the coordinates of each geometry, reduce the number of significant digits to the given number. Methods Return a geometry that represents the union of all geometries in the GeoSeries. Return minimum distance in meters between two lon/lat points. Returns a "simplified" version for each geometry using the Douglas-Peucker algorithm. Returns the Hausdorff distance between each geometry and other. Transform each arctern GeoSeries to GeoPandas GeoSeries. Transform each geometry to WKB formed bytes object. Transform each geometry to WKT formed string. Transform each geometry to a different coordinate reference system. Transform each to GeoJSON format string. Project-Id-Version: Arctern 
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2020-06-09 18:00+0800
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: zh_CN
Language-Team: zh_CN <LL@li.org>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 对于 GeoSeries 对象中的每个几何体，根据它创建一个新的有效的几何体。在构造新几何体过程中，不会删除原始几何体的任何顶点。如果原始几何体本来就是有效的，则直接返回原始几何体。 根据横坐标集合 `x` 和纵坐标集合 `y` 构造一组 POINT 对象。 对于 GeoSeries 对象中的每个几何体，计算它与 `other` 对象中相同位置的几何体之间交集。 对于 GeoSeries 对象中的每个几何体，判断它与 `other` 对象中相同位置的几何体之间的最短二维笛卡尔（平面）距离。 对于 GeoSeries 对象中的每个几何体，计算它的点的数量。 对于 GeoSeries 对象中的每个几何体，判断它是否与 `other` 对象中相同位置的几何体重叠。“重叠”表示两个几何体相交且不互相包含。 对于 GeoSeries 对象中的每个几何体，判断它是否与 `other` 对象中相同位置的几何体相邻。“相邻”表示两个几何体在边界上有共同的点。 对于 GeoSeries 对象中的每个几何体，判断它是否与 other 对象中相同位置的几何体相交。 对于 GeoSeries 对象中的每个几何体，判断它是否包含 `other` 对象中相同位置的几何体。 对于 GeoSeries 对象中的每个几何体，判断它是否与 `other` 对象中相同位置的几何体存在交集。 对于 GeoSeries 对象中的每个几何体，判断它是否与 `other` 对象中相同位置的几何体等价。“等价”表示两个几何体的几何结构相同。 对于 GeoSeries 对象中的每个几何体，判断它是否在 `other` 对象中相同位置的几何体的内部。 计算 GeoSeries 对象中每个几何体的中心点。 对于 GeoSeries 对象中的每个几何体，计算它的最小矩形边界范围。 计算包含一组几何体的最小矩形边界范围，且该矩形的边与坐标轴平行。 由 geopandas GeoSeries 构造几何体。 根据 GeoJson 字符串构造几何体。 对于 GeoSeries 对象中的每个几何体，根据给定的参数计算它的最小矩形边界范围，且该矩形的边与坐标轴平行。 对于 GeoSeries 对象中的每个几何体，计算它的近似表示。近似表示的方法是将每个几何图形中的曲线转换为近似线性表示。 对于 GeoSeries 对象中的每个几何体，计算包围它的最小的凸几何体。 对于 GeoSeries 对象中的每个几何体，创建一个与它的最远距离不大于 `distance` 的几何体。 对于 GeoSeries 对象中的每个几何体，根据指定的有效数字位数 `precision` 创建降低坐标精度后的几何体。 方法 返回一个代表一组几何体的并集的几何体。 对于 GeoSeries 对象中的每个几何体，根据经纬度坐标计算地球表面两点之间的最短球面距离。该方法使用 SRID 定义的地球和半径。 对于 GeoSeries 对象中的每个几何体，计算它的简化表示。简化表示的算法是 Douglas-Peucker 算法。 对于 GeoSeries 对象中的每个几何体，判断它与 `other` 对象中相同位置的几何体之间的 Hausdorff 距离。此距离用于度量两个几何体之间的相似度。 将 Arctern GeoSeries 转换为 GeoPandas GeoSeries。 将几何体转换为 WKB 格式的字节对象。 将几何体转换为 WKT 格式的字符串。 转换几何体的坐标参考系。 将每个几何体转换为 GeoJSON 格式的字符串。 