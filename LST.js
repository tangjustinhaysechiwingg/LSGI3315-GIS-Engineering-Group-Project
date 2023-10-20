// Land Surface Temperature Mapping on Google Earth Engine
// Written by Tang Justin Hayse Chi Wing G. 


// Cloud mask
function maskL8sr(col) {
  // Bits 3 and 5 are cloud shadow and cloud, respectively.
  var cloudShadowBitMask = (1 << 5);
  var cloudsBitMask = (1 << 3);
  // Get the pixel QA band.
  var qa = col.select('pixel_qa');
  // Both flags should be set to zero, indicating clear conditions.
  var mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0)
                .and(qa.bitwiseAnd(cloudsBitMask).eq(0));
  return col.updateMask(mask);
}


// Wrong boundary in Hong Kong (without Tsing Yi and Islands)
//var HKBorder = dataset.filter(ee.Filter.eq('country_na', 'Hong Kong'));
//print(HKBorder);
//Map.centerObject(HKBorder, 6);
//Map.addLayer(HKBorder);


// Parameter Setting 
var vizParams = {
bands: ['B5', 'B6', 'B4'],
min: 0,
max: 4000,
gamma: [1, 0.9, 1.1]
};

var vizParams2 = {
bands: ['B6'],
min: 0,
max: 3000,
gamma: 1.4,
};

//load the collection:
// {
//var col = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
//.map(maskL8sr)
//.filterDate('2018-05-01','2018-09-30')
//.filterBounds(geometry);
//}
//print(col, 'coleccion');

// Choosing the Summer Period in Hong Kong within 9 years 
var dataset_2022 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    .map(maskL8sr)
    .filterDate('2022-06-01', '2022-07-30')

  // .filter(ee.Filter.calendarRange(06,18,'hour'))
    .filterBounds(geometry2);
var dataset_2021 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    .map(maskL8sr)
    .filterDate('2021-06-01', '2021-09-30')

  // .filter(ee.Filter.calendarRange(06,18,'hour'))
    .filterBounds(geometry2);
var dataset_2020 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    .map(maskL8sr)
    .filterDate('2020-05-20', '2020-09-30')
 
  // .filter(ee.Filter.calendarRange(06,18,'hour'))
    .filterBounds(geometry2);
var dataset_2019 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    .map(maskL8sr)
    .filterDate('2019-05-20', '2019-09-30')

  // .filter(ee.Filter.calendarRange(06,18,'hour'))
    .filterBounds(geometry2);
var dataset_2018 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    .map(maskL8sr)
    .filterDate('2018-05-20', '2018-09-30')

  // .filter(ee.Filter.calendarRange(06,18,'hour'))
    .filterBounds(geometry2);
var dataset_2017 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    .map(maskL8sr)
    .filterDate('2017-05-20', '2017-09-30')

  // .filter(ee.Filter.calendarRange(06,18,'hour'))
    .filterBounds(geometry2);
var dataset_2016 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    .map(maskL8sr)
    .filterDate('2016-05-20', '2016-09-30')
  
  // .filter(ee.Filter.calendarRange(06,18,'hour'))
    .filterBounds(geometry2);
var dataset_2015 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    .map(maskL8sr)
    .filterDate('2015-05-20', '2015-09-30')

  // .filter(ee.Filter.calendarRange(06,18,'hour'))
    .filterBounds(geometry2);
var dataset_2014 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    .map(maskL8sr)
    .filterDate('2014-05-20', '2014-09-30')

    //.filter(ee.Filter.calendarRange(06,18,'hour'))
    .filterBounds(geometry2);
var dataset_2013 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    .map(maskL8sr)
    .filterDate('2013-05-20', '2013-09-30')

  // .filter(ee.Filter.calendarRange(06,18,'hour'))
    .filterBounds(geometry2);
    
var col = dataset_2022
        .merge(dataset_2021)
        .merge(dataset_2020)
        .merge(dataset_2019)
        .merge(dataset_2018)
        .merge(dataset_2017)
        .merge(dataset_2016)
        .merge(dataset_2015)
        .merge(dataset_2014)
        .merge(dataset_2013);
        print(col);

// Satellite Image Reduction (Take Median)
{
var image = col.median();
print(image, 'image');
Map.addLayer(image, vizParams2);  // Using Parameter Set 2
}

//NDVI Computation
{
var ndvi = image.normalizedDifference(['B5', 'B4']).rename('NDVI');
var ndviParams = {min: -1, max: 1, palette: ['blue', 'white', 'green']};
print(ndvi,'ndvi');
Map.addLayer(ndvi, ndviParams, 'ndvi');
}

//select thermal band 10(with brightness tempereature), no calculation 
var thermal= image.select('B10').multiply(0.1);
var b10Params = {min: 291.918, max: 302.382, palette: ['blue', 'white', 'green']};
Map.addLayer(thermal, b10Params, 'thermal');

// Maximum and Minimum of NDVI
{
var min = ee.Number(ndvi.reduceRegion({
reducer: ee.Reducer.min(),
geometry: geometry2,
scale: 30,
maxPixels: 1e9
}).values().get(0));
print(min, 'min');

var max = ee.Number(ndvi.reduceRegion({
reducer: ee.Reducer.max(),
geometry: geometry2,
scale: 30,
maxPixels: 1e9
}).values().get(0));
print(max, 'max')
}

// NDBI Computation
{
var ndbi = image.normalizedDifference(['B6', 'B5']).rename('NDBI');
var ndbiParams = {min: -1, max: 1, palette: ['red',"white", "green"]};
print(ndbi,'ndbi');
Map.addLayer(ndbi, ndbiParams, 'ndbi');
}

// Fractional Vegetation
{
var fv =(ndvi.subtract(min).divide(max.subtract(min))).pow(ee.Number(2)).rename('FV'); 
print(fv, 'fv');
Map.addLayer(fv);
}

// Emissivity
var a= ee.Number(0.004);
var b= ee.Number(0.986);
var EM = fv.multiply(a).add(b).rename('EMM');
var imageVisParam3 = {min: 0.9865619146722164, max:0.989699971371314};
Map.addLayer(EM, imageVisParam3,'EMM');

//Land Surface Temperature in Celsius Degree
var LST = thermal.expression(
'(Tb / (1 + (0.00115 * (Tb / 1.438)) * log(Ep)))-273.15', 
{
'Tb': thermal.select('B10'),
'Ep': EM.select('EMM')
})
.rename('LST');
Map.addLayer(LST, {min: 20, max:30, 
palette: [
'040274', '040281', '0502a3', '0502b8', '0502ce', 
'0502e6', '0602ff', '235cb1', '307ef3', '269db1', 
'30c8e2', '32d3ef', '3be285', '3ff38f', '86e26f', 
'3ae237', 'b5e22e', 'd6e21f', 'fff705', 'ffd611', 
'ffb613', 'ff8b13', 'ff6e08', 'ff500d', 'ff0000', 
'de0101', 'c21301', 'a71001', '911003' ]}, 
'LST')

// Build Output Directry
Export.image.toDrive({
  image: ndbi,
  description: 'ndbi',  //satellite image 
  scale: 30,
  region: geometry2,
  folder: "Downloads",
  fileFormat: 'GeoTIFF',
});
