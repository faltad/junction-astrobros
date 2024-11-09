import { Position } from "geojson";
export type SWandNE = { sw: Position; ne: Position } | null;

export function findSWandNECoordinates(
  coordinates: Position[][]
): SWandNE | null {
  if (!coordinates.length) return null;

  // Flatten the two-dimensional array and ensure each element is [lon, lat]
  const flattenedCoords = coordinates
    .flat()
    .map((coord) => coord.slice(0, 2) as [number, number]);

  // Initialize SW and NE points to the first coordinate in the flattened array
  const sw: Position = [...flattenedCoords[0]];
  const ne: Position = [...flattenedCoords[0]];

  flattenedCoords.forEach(([lon, lat]) => {
    // Update SW (southwestern-most) coordinate: minimum latitude and longitude
    if (lat < sw[1]) sw[1] = lat;
    if (lon < sw[0]) sw[0] = lon;

    // Update NE (northeastern-most) coordinate: maximum latitude and longitude
    if (lat > ne[1]) ne[1] = lat;
    if (lon > ne[0]) ne[0] = lon;
  });

  return { sw, ne };
}
