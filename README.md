# Betel - An image similarity network

**This is not an officially supported Google product.**

This repository is part of an intern project to explore the impact of
image-based features for app-app similarity.

## About
The project focuses on binary classifier which recognises apps from the "Music & Audio" Google Play Store category. The code also includes modules which help with retrieving data and building the sets needed for training.

## Flags
  `--scrape`: if True (default), scraping is performed  
  `--build`: if True (default), builds train-validation-test data sets  
  `--input_file`: CSV file with app ids (input for scraping stage)  
  `--scraper_storage_dir`: directory path for the output of the scraper (default ```./app_details```)  
  `--category_filter`: comma separated list of Play categories whose apps to keep (default: all categories found in the input data)  
  `--builder_storage_dir`: directory path for the output of the scraper (default ```./data_set```)  
  `--classes`: the desired classes for the classifier (default: all categories found in the input data)  
  `--batch_size`: model batch size (default 32)  
  `--target_img_dim`: size (for square images; default 192)  
  `--shuffle`: if True (default), shuffling on epoch end is performed  


## Needed directory structures
  After the scraping stage the `--scraper_storage_dir` should contain:
- `apps` file: CSV file with <app_id, category> columns
- the icons of all apps mentioned in the  `--input_file` parameter  

The input directory for the DataSetBuilder should have this structure.  

<br/>
  
  After building the data sets `--builder_storage_dir` should contain:
- the train-validation-test data sets, each having directories for every category
- an `info` directory having a CSV file per category with <app_id, data_set> columns  

The input directory for the ClassifierSequence should be one of the data sets.


## Usage
Here are some usage examples.

1. Scraping, bulding the data sets and training the model  

    - `--input_file` is the only parameter needed.  
    `PYTHONPATH=$PYTHONPATH:. python betel/main.py --input_file=path/to/dir/input.csv`

2. Building the data sets and training the model  

    - Either the specified `--scraper_storage_dir` directory or the default `./app_details` directory needs to have the above mentioned structure.  
    `PYTHONPATH=$PYTHONPATH:. python betel/main.py --scrape=False [--scraper_storage_dir=path/to/dir/]`

3. Training the model  

    - Either the specified `--builder_storage_dir` directory or the default `./data_set` directory needs to have the above mentioned structure.  
    `PYTHONPATH=$PYTHONPATH:. python betel/main.py --scrape=False --build=False [--builder_storage_dir=path/to/dir/]`  

<br/>

If apps from unspecified classes are found in the input data when using the `--classes` parameter, they are automatically put under the 'others' category.

## Limitations
  The categories specified in `--category_filter` and `--classes` parameters must be Google Play Store ones. The exact strings for every categories can be found in the `play_store_categories` enum.

