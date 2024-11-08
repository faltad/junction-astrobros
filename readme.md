# AstroBros


## Investigating tool for ecological disaster  

Example: https://blackdotsolutions.com/blog/using-osint-in-environmental-investigations/

Idea is to build a website/tool that would help any concerned citizen/investigator/agency to find the root cause of a 
disaster, such as oil spill, illegal logging, contamination of rivers etc.

We would focus only on one or two scenarios during the hackaton, while plan for more.



## Other idea: hotzones mapping + timeline

Imagine a map of the world with an overlay that would show the impact of a zone on greenhouse gas emissions.
- fetch and aggregate the 10 most impacting greenhouse gases.
- calculate a index of pollution per area (zoom / unzoom etc)
- divide this index per inhabitants
- Automated detection of hotspots / outliers
- And importantly, show a timeline to assess possible policy changes and their results on the index.



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
