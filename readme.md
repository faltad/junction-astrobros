# AstroBros


## Investigating tool for ecological disaster  

Example: https://blackdotsolutions.com/blog/using-osint-in-environmental-investigations/

Idea is to build a website/tool that would help any concerned citizen/investigator/agency to find the root cause of a 
disaster, such as oil spill, illegal logging, contamination of rivers etc.

During the hackaton, we will focus on two solutions:
- oil spill
- deforestation / illegal logging

Steps:
- Find a recent oil spill and the coordinates. Find a zone without oil spill.
- Find a place with deforestation + a zone without.
- search online for possible methodology to analyze oilspills (https://www.bellingcat.com/resources/how-tos/2024/08/30/marine-oil-spill-detection-guide/)
- same for illegal logging / forest cover change
- find data source from Sentinel 2 and see if possible to fetch historical data for a specified zone -> this is "visual data"
- build a basic UI that would enable to see a map and select places.
- For now, we will only enable the tool for the coordinates found above.




### Illegal logging tool

- Be able to pick an area (first step hardcoded area)
- get the data for a given timeline (also hardcoded)
- apply different algorithm/models to describe forest loss / whatever
- 


### Tooling
Backend:
- python
- mongo

### Data sources

- Copernicus:
  - Co2 -> 
  - Methane
  - Nitrous oxide
  - Fluorinated gases
  - Deforestation/Land use changes (??)
  - soot / black carbon
  - Ozone 
  - Albedo Effect (Changes in Earth's Reflectivity)
  - Water Vapor
  - Urban heat islands
- AIS for boat localizations
