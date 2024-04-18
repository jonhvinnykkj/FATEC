
// Define the date range
var startDate = '2018-01-01';
var endDate = '2023-12-31';

// Filter the Sentinel-2 image collection
var sentinel2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(talhao1)
  .filterDate(startDate, endDate)
  .filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', 10)
  .select(['B8', 'B4', 'B3', 'B11', 'TCI_R', 'TCI_G', 'TCI_B']);

// Calculate NDVI
var calculateNDVI = function(image) {
  var NDVI = image.normalizedDifference(['B8', 'B4']).rename('NDVI');
  return NDVI.set('system:time_start', image.get('system:time_start'));
};

var calculateGCI = function(image) {
  var GCI = image.normalizedDifference(['TCI_G', 'TCI_B']).rename('GCI');
  return GCI.set('system:time_start', image.get('system:time_start'));
}

var calculateNDWI = function(image) {
  var NDWI = image.normalizedDifference(['B3', 'B8']).rename('NDWI');
  return NDWI.set('system:time_start', image.get('system:time_start'));
}

var calculateNDMI = function(image) {
  var NDMI = image.normalizedDifference(['B8', 'B11']).rename('NDMI');
  return NDMI.set('system:time_start', image.get('system:time_start'));
}

// Apply NDVI calculation to the image collection
var ndviCollection = sentinel2.map(calculateNDVI);

// Create a chart of NDVI over time
var chartNDVI = ui.Chart.image.seriesByRegion({
  imageCollection: ndviCollection,
  regions: talhao1,
  reducer: ee.Reducer.median(),
  band: 'NDVI',
  scale: 10,
  xProperty: 'system:time_start'
});

var chartGCI = ui.Chart.image.seriesByRegion({
  imageCollection: sentinel2.map(calculateGCI),
  regions: talhao1,
  reducer: ee.Reducer.median(),
  band: 'GCI',
  scale: 10,
  xProperty: 'system:time_start'
});

var chartNDWI = ui.Chart.image.seriesByRegion({
  imageCollection: sentinel2.map(calculateNDWI),
  regions: talhao1,
  reducer: ee.Reducer.median(),
  band: 'NDWI',
  scale: 10,
  xProperty: 'system:time_start'
});

var chartNDMI = ui.Chart.image.seriesByRegion({
  imageCollection: sentinel2.map(calculateNDMI),
  regions: talhao1,
  reducer: ee.Reducer.median(),
  band: 'NDMI',
  scale: 10,
  xProperty: 'system:time_start'
});

// Defina o intervalo de anos
var startYear = 2018;
var endYear = 2023;

// Função para obter a imagem média de um ano específico
var getYearlyImage = function(year) {
  var startDate = ee.Date.fromYMD(year, 1, 1);
  var endDate = startDate.advance(1, 'year');

  var image = sentinel2
    .filterDate(startDate, endDate)
    .mean() // calcula a média das imagens do ano
    .set('year', year); // adiciona o ano como uma propriedade da imagem

  // Verifique se as bandas existem na imagem
  var bands = image.bandNames();
  if (bands.contains('B8') && bands.contains('B4') && bands.contains('TCI_R')) {
    return image.select(['B8', 'B4', 'TCI_R']);
  } else {
    print('Image for year ' + year + ' does not have all required bands.');
    return null;
  }
};

// Itera sobre os anos e adiciona cada imagem ao mapa
for (var year = startYear; year <= endYear; year++) {
  var image = getYearlyImage(year);
  if (image) {
    // Exporta a imagem para o Google Drive
    Export.image.toDrive({
      image: image,
      description: 'Image_' + year,
      scale: 30,
      region: talhao1,
      maxPixels: 1e13
    });
  }
}

// Create a chart of median NDVI over time
var chartMedianNDVI = ui.Chart.image.seriesByRegion({
    imageCollection: ee.ImageCollection.fromImages([ndviMedian]),
    regions: talhao1,
    reducer: ee.Reducer.median(),
    band: 'NDVI',
    scale: 10,
    xProperty: 'system:time_start'
  });
  
  // Create a chart of median GCI over time
  var chartMedianGCI = ui.Chart.image.seriesByRegion({
    imageCollection: ee.ImageCollection.fromImages([gciMedian]),
    regions: talhao1,
    reducer: ee.Reducer.median(),
    band: 'GCI',
    scale: 10,
    xProperty: 'system:time_start'
  });
  
  // Create a chart of median NDWI over time
  var chartMedianNDWI = ui.Chart.image.seriesByRegion({
    imageCollection: ee.ImageCollection.fromImages([ndwiMedian]),
    regions: talhao1,
    reducer: ee.Reducer.median(),
    band: 'NDWI',
    scale: 10,
    xProperty: 'system:time_start'
  });
  
  // Create a chart of median NDMI over time
  var chartMedianNDMI = ui.Chart.image.seriesByRegion({
    imageCollection: ee.ImageCollection.fromImages([ndmiMedian]),
    regions: talhao1,
    reducer: ee.Reducer.median(),
    band: 'NDMI',
    scale: 10,
    xProperty: 'system:time_start'
  });
  
  // Print the charts
  print(chartMedianNDVI);
  print(chartMedianGCI);
  print(chartMedianNDWI);
  print(chartMedianNDMI);
// Add the chart and region to the map
Map.addLayer(talhao1);
Map.centerObject(talhao1, 17);
print(chartNDVI);
print(chartGCI);
print(chartNDWI);
print(chartNDMI);