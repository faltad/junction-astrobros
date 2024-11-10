## Oil spill documentation

The Sentinel-1 mission was designed as a constellation of two satellites: Sentinel-1A launched on 3 April 2014 and Sentinel-1B, launched on 25 April 2016. The satellites are in synchronous orbit with the Sun at an altitude of 693 km, with an inclination of 98.18°. Each satellite is equipped with an advanced C-SAR radar, regardless of weather conditions. The Sentinel-1 mission was developed to ensure the continuity of Earth’s radar mapping. It is characterized by a short revisit time, which is 12 days. This makes the mission suitable for monitoring land and ocean surface changes, as well as for security and emergency responses [36]. Sentinel-2 is a European mission for multi- and multi-spectral imaging with wide-range data acquisition and high resolution. It consists of two satellites, rotating in the same orbit synchronized with the movement of the Sun, 180 ° apart from each other. The position of each satellite is measured by a dual-frequency Global Navigation Satellite System (GNSS) receiver. The full specification is designed to ensure a high reimaging frequency of 5 days at the equator. This guarantees the continuity of data collection and delivery.

For the purposes of this work, the following indices were used:
NDVI
NDVI=NIR−REDNIR+RED
NDVI is an indicator for determining the state of vegetation [38,39,40]. NDVI is based on the contrast between the greatest near infrared reflection and the red absorption. The range of NDVI values is −1 to 1. Negative NDVI values (values close to −1) correspond to water. Values close to zero (−0.1–0.1) correspond to barren regions of rock, sand, or snow. Low, positive values are for shrubs and grasslands (values from about 0.2 to 0.4), while high values are for moderate and tropical rainforests (values close to 1).
NDWI2
NDWI2=GREEN−NIRGREEN+NIR
(2)
NDWI2 is used to monitor changes in water content in water reservoirs. Since water reservoirs strongly absorb light in the visible and infrared electromagnetic spectrum, green and near infrared bands are used to illuminate water reservoirs. Index values greater than 0.3 usually relate to water bodies. The higher the value, the greater the content of healthy water in a given tank. On the other hand, results below 0.3 indicate no water [41].
NDSII
NDSII=RED−SWIRRED+SWIR
(3)
NDSII relies on the ratio of visible and shortwave infrared wavelengths to separate snow/ice pixels from cloud cover and other undesirable elements. It is calculated by dividing the red and short infrared bands by their sum, because snow indicates the lowest and the highest reflectance in these bands, respectively. The index values range from −1 to 1. When surveying areas covered with a significant amount of snow, including Alaska, Minnesota, and Iceland, the NDSI mapped the snow cover well and distinguished it from clouds for a value of about 0.4 [42].
SWM
SWM=BLUE+GREENNIR+SWIR
(4)
SWM provides fast and effective water detection. It is dedicated to Sentinel-2 products. It is calculated as the sum of the blue and green bands divided by the sum of the near and short infrared bands. The range of index values is from 0–12, and the optimal threshold is values in the range 1.4–1.6, when the index reaches an accuracy of 96–99% depending on the test area [43].
