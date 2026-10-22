# Publication checklist

Repository: [https://github.com/raflialfansyah/climate-informed-hotspot-models](https://github.com/raflialfansyah/climate-informed-hotspot-models). Contents remain local until a commit is pushed and public access is verified. The manuscript and reviewer forms are outside this repository.

## Local package checks

- [x] Use the adopted main same-day notebook, with all scientific stages off by default.
- [x] Retain MIT for software and guides, with data and third-party attribution described separately.
- [x] Include processed daily aggregates, full SST context and saved results under the agreed Option 2 scope.
- [x] Identify NOAA OISST v2.1 and regional processing from the confirmed manuscript and author-supplied MATLAB scripts, with exact SST-context checks.
- [x] Record the author's ERA5 single-level source URL and the current CDS licence and attribution.
- [x] Exclude raw grids, fitted model snapshots, private paths, runtime outputs, GADM coordinates and the standalone GADM map.
- [x] Keep source-calendar, unit, sensor-coverage and retrieval qualifications explicit; do not change scientific inputs to fill metadata gaps.

Technical checks are recorded in `../validation/RELEASE_VALIDATION_REPORT.md` and `../validation/`. Source policies and modification notices are in `SOURCE_ATTRIBUTION.md`. The OISST version and extraction rules are documented by the supplied scripts; actual original-grid downloads and processing have not been rerun.

## Publication steps

- [ ] Authors review contributor names and the software citation as part of their normal release review.
- [ ] Create the initial commit and push the verified local package to the existing repository.
- [ ] Verify public access to the notebook, processed inputs, saved results and source notices.
- [ ] Add the working public link to the manuscript and Reviewer 1 N05 and Reviewer 2 m6 responses.

The repository does not contain an optimized cross-model ensemble. No ensemble-composition experiment remains pending. A DOI may be added after a versioned archive is created; none is claimed here.
