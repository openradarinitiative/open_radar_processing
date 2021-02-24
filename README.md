# Open Radar Processing
This repository contains the "Open Radar Initiative" processing and contains utilites to read the raw UDP stream from Texas Instruments' DCA1000, dump the raw data to the harddrive and the ability to play them back later. 
The datacube parameters are stored in _params.py_. 

The examples included are:
### Receive and log raw data
This is done by _receive_and_log_raw_data.py_ and requires that the radar has been configured and the stream is started. 
This can be done by using the software supplied in https://github.com/openradarinitiative/openradar_mmwave_utils or by using the ".lua" script in combination with mmWaveStudio.

### Show range Doppler from openradar file
This is done by using _play_from_openradar_file.py_ which plays a file logged by the previous script and shows a range-Doppler map.

### Show range Doppler from TI file
This is done by _play_from_ti_file.py_ which loads the raw data from TI's ".bin" recorded by using the ".lua" script in https://github.com/openradarinitiative/openradar_mmwave_utils.
The loaded raw data is processed to show a range-Doppler map. 

### Convert TI's format to ".open_radar"
This is performed by _convert_bin_to_open_radar.py_
