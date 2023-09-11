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
  title  = {Glass Curtain Wall Installation Dataset},
  year   = {2023},
  doi    = {10.26180/23538198},
  url    = {https://github.com/Brandon-Johns/glass-curtain-wall-installation-dataset},
}
```

This work is companion to [our publication](https://doi.org/10.1016/j.measurement.2023.113459)
```bibtex
@Article{citeKey,
  author  = {Brandon Johns and Elahe Abdi and Mehrdad Arashpour},
  journal = {Measurement},
  title   = {Crane payload localisation for curtain wall installation: A markerless computer vision approach},
  year    = {2023},
  issn    = {0263-2241},
  pages   = {113459},
  volume  = {221},
  doi     = {10.1016/j.measurement.2023.113459},
}
```

(Optional) If you find this work to be useful, please message me and share how you used it. I'd love to hear about it. 
You can find me here: [twitter](https://twitter.com/BrandonJohns96), [linkedin](https://www.linkedin.com/in/brandon-johns-6bab7815a).


## Acknowledgments
This research was supported by an Australian Government Research Training Program (RTP) Scholarship. This research is supported by Building 4.0 CRC. The support of the Commonwealth of Australia through the Cooperative Research Centre Programme is acknowledged.

## License
This work is distributed under the [BSD-3-Clause License](./LICENSE.txt)

The dataset, user guide, and documentation are distributed under the [Creative Commons CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/)

The Building 4.0 CRC makes no warranty with regard to the accuracy of the information provided and will not be liable if the information is inaccurate, incomplete or out of date nor be liable for any direct or indirect damages arising from its use. The contents of this publication should not be used as a substitute for seeking independent professional advice.
