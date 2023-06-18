# Glass Curtain Wall Installation Dataset
A unitised curtain wall is a type of exterior wall for high-rise buildings, which is comprised of prefabricated modules that hang from the building floor slabs. This dataset depicts a partially installed unitised curtain wall.

The dataset consists of
- 140 images depicting a partially installed unitised curtain wall
- The camera calibration parameters
- Measurement of the pose (position and orientation) of the camera with respect to the wall
- Ground truth images for 60 images from the dataset, segmented as [glass, frame, other]

The dataset is primarily intended to be used in the development of systems to automatically measure the relative pose between the camera and the wall; systems to identify the location where the next curtain wall module should be installed; and related user interfaces.

## Documentation
Please see [the user guide](./UserGuide.pdf).

## Citation
Please cite this work as
```bibtex
@Dataset{citeKey,
  author = {Johns, Brandon and Abdi, Elahe and Arashpour, Mehrdad},
  doi    = {10.26180/23538198},
  title  = {Glass Curtain Wall Installation Dataset},
  url    = {https://github.com/Brandon-Johns/glass-curtain-wall-installation-dataset},
  year   = {2023},
}
```

## Acknowledgments
This research was supported by an Australian Government Research Training Program (RTP) Scholarship. This research is supported by Building 4.0 CRC. The support of the Commonwealth of Australia through the Cooperative Research Centre Programme is acknowledged.

## License
This work is distributed under the [BSD-3-Clause License](./LICENSE.txt)

The images and motion capture data are licenced under the [Creative Commons CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/)
