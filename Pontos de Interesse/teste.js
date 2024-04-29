var Faixa1 = table.filter(ee.Filter.eq('LAYER', 'Faixa 1')).first();
var Faixa2 = table.filter(ee.Filter.eq('LAYER', 'Faixa 2')).first();
var Faixa3 = table.filter(ee.Filter.eq('LAYER', 'Faixa 3')).first();
var Faixa4 = table.filter(ee.Filter.eq('LAYER', 'Faixa 4')).first();
var Faixa5 = table.filter(ee.Filter.eq('LAYER', 'Faixa 5')).first();
var Faixa6 = table.filter(ee.Filter.eq('LAYER', 'Faixa 6')).first();
var Faixa7 = table.filter(ee.Filter.eq('LAYER', 'Faixa 7')).first();
var Faixa8 = table.filter(ee.Filter.eq('LAYER', 'Faixa 8')).first();
var Faixa9 = table.filter(ee.Filter.eq('LAYER', 'Faixa 9')).first();

var Faixas = ee.FeatureCollection([
  ee.Feature(Faixa1.geometry(), {label: 'Faixa 1'}),
  ee.Feature(Faixa2.geometry(), {label: 'Faixa 2'}),
  ee.Feature(Faixa3.geometry(), {label: 'Faixa 3'}),
  ee.Feature(Faixa4.geometry(), {label: 'Faixa 4'}),
  ee.Feature(Faixa5.geometry(), {label: 'Faixa 5'}),
  ee.Feature(Faixa6.geometry(), {label: 'Faixa 6'}),
  ee.Feature(Faixa7.geometry(), {label: 'Faixa 7'}),
  ee.Feature(Faixa8.geometry(), {label: 'Faixa 8'}),
  ee.Feature(Faixa9.geometry(), {label: 'Faixa 9'}),
]);



// Function to mask clouds using the Sentinel-2 QA band
function maskS2clouds(image){
  var qa = image.select('QA60');
    
  // Bits 10 and 11 are clouds and cirrus, respectively.
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;
    
  // Both flags should be set to zero, indicating clear conditions.
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
     .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
     
  return image.updateMask(mask).divide(10000).copyProperties(image).set('system:time_start', image.get('system:time_start'));
}

// Obtendo as imagens de Sentinel-2 para o talhão todo
var dataset = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                     .filterDate('2023-04-01', '2024-04-20')
                     .filter(ee.Filter.bounds(table.geometry()))
                     // pre-filter to get less cloudy granules
                     .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
                     .map(maskS2clouds);
                     
// NDVI da area toda
var addNDVI = function(image){
  var date = image.date();
  var years = date.difference(ee.Date('1970-01-01'), 'year');
  return image
    .addBands(image.normalizedDifference(['B8','B4']).rename('NDVI'))
    .addBands(ee.Image(years).rename('time')).float()
    .addBands(ee.Image.constant(1));
};

// adciona camada de NDVI
var dataset = dataset.map(addNDVI);

// cria um conjunto de imagens somente com NDVI
var NDVI = dataset.select(['NDVI']);

// adciona a mediana do NDVI
var NDVImed = NDVI.median();
//transforma as faixas em geometrias de faixas distintas, seguindo as mediçoes feitas
var geometry = Faixas.geometry();
var allFaixas = [Faixa1, Faixa2, Faixa3, Faixa4, Faixa5, Faixa6, Faixa7, Faixa8, Faixa9];
var combinedReducer = ee.Reducer.minMax().combine({
  reducer2: ee.Reducer.mean(),
  sharedInputs: true
});

//grafico de cada faixa
allFaixas.forEach(function(faixa, index) {
  var chart = ui.Chart.image.series({
    imageCollection: NDVI,
    region: faixa.geometry(),
    reducer: combinedReducer,
    scale: 10
  }).setOptions({
    title: 'NDVI ao longo do tempo - Faixa ' + (index + 1),
    hAxis: {title: 'Data'},
    vAxis: {title: 'NDVI'}
  });

  print(chart);
});

// grafico de todas as faixas juntas
var chartAll = ui.Chart.image.series({
  imageCollection: NDVI,
  region: Faixas.geometry(),
  reducer: combinedReducer,
  scale: 10
}).setOptions({
  title: 'NDVI ao longo do tempo - Todas as Faixas',
  hAxis: {title: 'Data'},
  vAxis: {title: 'NDVI'}
});

print(chartAll);

var NDVICollection = dataset.map(function(image) {
  var stats = image.select('NDVI').reduceRegion({
    reducer: ee.Reducer.minMax().combine({
      reducer2: ee.Reducer.mean(),
      sharedInputs: true
    }),
    geometry: Faixas.geometry(),
    scale: 10
  });

  return image.select('NDVI').set(stats);
});

Map.addLayer(NDVImed, {min: -1, max: 1, palette: ['blue', 'white', 'green']}, 'NDVI');
Map.addLayer(Faixas, {}, 'Faixas');
Map.centerObject(Faixas, 10);

var faixasList = Faixas.toList(Faixas.size());
for (var i = 0; i < faixasList.size().getInfo(); i++) {
  var faixa = ee.Feature(faixasList.get(i));
  var statsCollection = NDVI.map(function(image) {
    var stats = image.reduceRegion({
      reducer: ee.Reducer.minMax().combine({
        reducer2: ee.Reducer.mean(),
        sharedInputs: true
      }),
      geometry: faixa.geometry(),
      scale: 10
    });
    return ee.Feature(null, stats).set('date', image.date().format('YYYY-MM-dd'));
  });
  Export.table.toDrive({
    collection: statsCollection,
    description: 'NDVI_stats_faixa_' + (i + 1),
    fileFormat: 'CSV'
  });
}

var statsCollectionTotal = NDVI.map(function(image) {
  var stats = image.reduceRegion({
    reducer: ee.Reducer.minMax().combine({
      reducer2: ee.Reducer.mean(),
      sharedInputs: true
    }),
    geometry: Faixas.geometry(),
    scale: 10
  });
  return ee.Feature(null, stats).set('date', image.date().format('YYYY-MM-dd'));
});

// exporta os dados de NDVI por dia e por faixa para um arquivo CSV
Export.table.toDrive({
  collection: statsCollectionTotal,
  description: 'NDVI_stats_total',
  fileFormat: 'CSV'
});

// exporta as imagens dos indices de NDVI de cada dia como CSV tambem
var imageList = dataset.toList(dataset.size());

// mapeia a lista de imagens para obter as datas
var dates = imageList.map(function(image) {
  return ee.Image(image).date().format('YYYY-MM-dd');
});
dates = dates.getInfo();

for (var i = 0; i < imageList.size().getInfo(); i++) {
  var image = ee.Image(imageList.get(i));
  var date = dates[i];

  var features = image.reduceToVectors({
    geometry: Faixas.geometry(),
    scale: 10,
    geometryType: 'centroid'
  });
  Export.table.toDrive({
    collection: features,
    description: 'NDVI_pixels_' + date,
    fileFormat: 'CSV'
  });
} 