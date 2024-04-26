var table = ee.FeatureCollection("projects/ee-interessepontos/assets/Faixas"),
    faixa1 = /* color: #98ff00 */ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Polygon(
                [[[-48.967633005676184, -21.360747671292934],
                  [-48.96698163176088, -21.364116455100554],
                  [-48.96672950411348, -21.36406649711715],
                  [-48.96732495451479, -21.36095907705981]]]),
            {
              "system:index": "0"
            })]);

Map.centerObject(table, 10);

var rgbVis = {
  bands: ['B11', 'B8', 'B3'],
  min: 0,
  max: 3000
};

var datasettalhao = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
              .filterDate('2023-03-01', '2024-04-20')
              .filterBounds(talhao)
              .filter(ee.Filter.lt("CLOUD_PIXEL_PERCENTAGE", 10))

print(datasettalhao)

var nirBand = 'B8';
var redBand = 'B4';
function calculateNDVI(image) {
  return image.normalizedDifference([nirBand, redBand]).rename('NDVI');
}

// Calculate NDVI for the image collection
var ndviCollection = datasettalhao.map(calculateNDVI);

// Get the median NDVI image
var medianNdvi = ndviCollection.median();

// Define visualization parameters for NDVI
var ndviVis = {
  min: -1,
  max: 1,
  palette: ['blue', 'white', 'green']
};

// Add NDVI to map
Map.addLayer(medianNdvi.visualize(ndviVis), {}, 'NDVI');
