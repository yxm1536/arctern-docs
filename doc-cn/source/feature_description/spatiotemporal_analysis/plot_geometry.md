# 绘图方法

本文档介绍 Arctern 的绘图方法。

## [plot_geometry](../../api_reference/plot/api/arctern.plot.plot_geometry.html)

### 方法定义

```python
   def plot_geometry(ax, geoms, **style_kwds)
```
### 参数介绍

* **ax:** matplotlib.axes._subplots.AxesSubplot 的实例，表示用于绘图的画布。
* **geoms:** 当前要绘制的几何图形集合，接受 pandas Series、Arctrn GeoSeries 或者 pandas DataFrame 作为输入。其中的几何图形元素必须是 WKB 形式。
* **style_kwds:** 绘图风格参数，包括：
  * **linewidth:** 线或多边形的线宽
  * **linestyle:** 线或多边形的线型
  * **edgecolor:** 多边形的边缘颜色
  * **facecolor:** 多边形的填充颜色
  * **color:** 点或线的颜色
  * **marker:** 点的形状
  * **markersize:** 点的大小
  * **alpha:** 透明度

以下展示如何使用 [plot_geometry](../../api_reference/plot/api/arctern.plot.plot_geometry.html) 方法绘制几何图形。


## 安装依赖库
```bash
conda install -c conda-forge descartes
conda install -c conda-forge matplotlib
```

## 生成测试数据

使用 GeoSeries 的构造函数创建一些几何体对象，包括点（POINT）、线（LINESTRING）、多边形（POLYGON）、多点（MULTIPOINT）、多个多边形（MULTIPOLYGON）、几何体集合（GEOMETRYCOLLECTION）和多线（MULTILINESTRING）。在后续步骤中，我们将演示如何绘制这些几何图形。

```python
>>> from arctern import GeoSeries
>>> 
>>> point_s = GeoSeries(["POINT (3 4)"])
>>> linestring_s = GeoSeries(["LINESTRING (0 0,1 1,2 3)"])
>>> polygon_s = GeoSeries(["POLYGON ((0 0,0 1,1.5 2,0 0))"])
>>> multi_point_s = GeoSeries(["MULTIPOINT (3 4,5 5)"])
>>> multi_linestring_s = GeoSeries(["MULTILINESTRING ((0 0,1 1,2 3),(1 0,2 4))"])
>>> multi_polygon_s = GeoSeries(["MULTIPOLYGON (((0 0,0 1,1.5 2,0 0)),((0 0,0 2,1 0,0 0)))"])
>>> geom_collection_s = GeoSeries(["GEOMETRYCOLLECTION("
...                     "polygon((1 1,1 2,2 2,2 1,1 1)),"
...                     "linestring(0 1, 5 6, 10 11),"
...                     "POINT(4 7))"])
>>> geoms = GeoSeries(["MULTILINESTRING ((0 0,1 1,2 3),(1 0,2 4))","POINT (3 4)","POLYGON ((0 0,0 1,1.5 2,0 0))"])
```


## 绘制几何图形

### 点

- **颜色：** 蓝
- **透明度：** 0.4
```python
>>> from arctern import plot
>>> import matplotlib.pyplot as plt
>>> fig,ax = plt.subplots()
>>> ax.grid()
>>> plot.plot_geometry(ax,point_s,color=["blue"],alpha=0.4)
>>> plt.show()
```

![](./img/point_s.png)

### 线

- **颜色：** 蓝
- **线型：** " -. "
- **透明度：** 0.4

```python
>>> from arctern import plot
>>> import matplotlib.pyplot as plt
>>> fig,ax = plt.subplots()
>>> ax.grid()
>>> plot.plot_geometry(ax,linestring_s,color=["blue"],linestyle=["-."],alpha=0.4)
>>> plt.show()
```

![](./img/linestring_s.png)

### 多边形

- **填充颜色：** 绿
- **线宽：** 3.0
- **边缘颜色：** 红
- **透明度：** 0.4

```python
>>> from arctern import plot
>>> import matplotlib.pyplot as plt
>>> fig,ax = plt.subplots()
>>> ax.grid()
>>> plot.plot_geometry(ax,polygon_s,facecolor=["green"],linewidth=3.0,edgecolor=["red"],alpha=0.4)
>>> plt.show()
```

![](./img/polygon_s.png)

### 多点

- **颜色：** 蓝
- **点型：** " * "
- **大小：** 40.0
- **透明度：** 0.4

```python
>>> from arctern import plot
>>> import matplotlib.pyplot as plt
>>> fig,ax = plt.subplots()
>>> ax.grid()
>>> plot.plot_geometry(ax,multi_point_s,color=["blue"],marker="*",markersize=40.0,alpha=0.4)
>>> plt.show()
```

![](./img/multi_point_s.png)

### 多线

- **颜色：** 蓝
- **线型：** " -- "
- **透明度：** 0.4

```python
>>> from arctern import plot
>>> import matplotlib.pyplot as plt
>>> fig,ax = plt.subplots()
>>> ax.grid()
>>> plot.plot_geometry(ax,multi_linestring_s,color=["blue"],linestyle=["--"],alpha=0.4)
>>> plt.show()
```

![](./img/multi_linestring_s.png)

### 多个多边形


- **填充颜色：** 蓝
- **透明度：** 0.4

```python
>>> from arctern import plot
>>> import matplotlib.pyplot as plt
>>> fig,ax = plt.subplots()
>>> ax.grid()
>>> plot.plot_geometry(ax,multi_polygon_s,facecolor=["blue"],alpha=0.4)
>>> plt.show()
```

![](./img/multi_polygon_s.png)

### 几何体集合

- **填充颜色：** 蓝
- **边缘颜色：** 红
- **点线颜色：** 绿
- **透明度：** 0.4

```python
>>> from arctern import plot
>>> import matplotlib.pyplot as plt
>>> fig,ax = plt.subplots()
>>> ax.grid()
>>> plot.plot_geometry(ax,geom_collection_s,facecolor=["blue"],edgecolor=["red"],color=["green"],alpha=0.4)
>>> plt.show()
```

![](./img/geom_collection_s.png)

### 多个几何图形

- **多线**
  * **线型：** " -. "
  * **颜色：** 蓝
- **多边形**
  * **线型：** 虚线 
  * **填充颜色：** 绿 
  * **边缘颜色**： 红
  * **点型：** " o "
  * **透明度：** 0.4

```python
>>> from arctern import plot
>>> import matplotlib.pyplot as plt
>>> fig,ax = plt.subplots()
>>> ax.grid()
>>> plot.plot_geometry(ax,geoms,linestyle=["-.","","--"],marker="o",color=["blue","red","green"],edgecolor=["","","red"],alpha=0.4)
>>> plt.show()
```

![](./img/geoms.png)

### 多次绘制几何图形

- **线**
   * **颜色：** 蓝
   * **线型：** " -. "
   * **透明度：** 0.4
- **多边形**
   * **填充颜色：** 绿
   * **线宽：** 3.0
   * **边缘颜色：** 红
   * **透明度：** 0.4
- **几何体集合**
   * **填充颜色：** 蓝
   * **边缘颜色：** 红
   * **点线颜色：** 绿
   * **透明度：** 0.4

```python
>>> from arctern import plot
>>> import matplotlib.pyplot as plt
>>> fig,ax = plt.subplots()
>>> ax.grid()
>>> plot.plot_geometry(ax,linestring_s,color=["blue"],linestyle=["-."],alpha=0.4)
>>> plot.plot_geometry(ax,polygon_s,facecolor=["green"],linewidth=3.0,edgecolor=["red"],alpha=0.4)
>>> plot.plot_geometry(ax,geom_collection_s,facecolor=["blue"],edgecolor=["red"],color=["green"],alpha=0.4)
>>> plt.show()
```

![](./img/multi_plot.png)
