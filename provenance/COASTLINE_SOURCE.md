# Coastline source and display geometry

The author identified GADM as the upstream map-boundary source on 21 October 2026. Cartopy was used in the mapping workflow. The author's description was: "the coastline is captured by defining a 5 km buffer from the outskirts". This record preserves the supplied description without inferring an inward or outward buffering operation, projection, administrative level or exact geometric construction.

Source: [GADM](https://gadm.org/). This is a creator attribution; the original GADM release, download filename, boundary level, processing script and Cartopy version have not been inspected. A metric buffer requires an appropriate distance calculation, but its implementation is not established by the attribution alone. No download of a current GADM release is substituted for the original source.

The initial candidate's `data/derived/figure_inputs.npz` contained a `coast` array with 14,301 segments, each with two longitude/latitude endpoints. Those segments were recovered from the peer-provided map figure and are used to reproduce its outlines. Recovery from the figure and the newly supplied upstream attribution are separate steps in the provenance chain. The saved segments have not been compared with the original GADM buffer output.

The geometry provides visual orientation in Figure 1. It does not define the model's hotspot-grid counts, regional masks or a verified land mask. It also does not resolve the original hotspot-data acquisition, point-to-cell binning, sensor coverage or filtering qualifications in Reviewer 4 request D01.

## Use and redistribution

[GADM's license page](https://gadm.org/license.html), consulted on 21 October 2026, allows academic and other non-commercial use and explicitly allows maps in academic research articles. Its general terms require prior permission for redistribution of the data or commercial use. The page's Austria-specific exception does not establish an exception for these Indonesian boundaries.

Publishing a map in an academic article and distributing reusable boundary coordinates in a GitHub repository are different uses. The article-map permission does not by itself authorize redistribution of the `coast` array, and creating a buffer or recovering paths from a figure does not establish a new MIT license for the geometry. Obtain permission or confirm an applicable exception before including reusable GADM-derived coordinates publicly; alternatively, exclude that geometry and document authorized local acquisition. Sharing of rendered figure assets should be assessed separately under their applicable terms.

The initial attribution-only update retained the geometry without changing it. The later Option 2 packaging below excludes that geometry from the public payload. No public upload, new buffer, manuscript change or model fitting has occurred. Software remains MIT-licensed, with the existing separate data and figure scope.

## Current Option 2 packaging

The public candidate no longer includes `coast` in `data/derived/figure_inputs.npz` or the original `figures/main/study-area-integrated.pdf`. Their initial copies are preserved in the private before-edit archive. All remaining NPZ arrays are unchanged; exact transformations and retained-array digests are in `CURRENT_TRANSFORMATIONS.json`. The manuscript itself is not changed. The optional local plotting input is supplied through `HOTSPOT_COASTLINE_PATH`; the runner otherwise skips Figure 1 rather than substituting a different coastline.
