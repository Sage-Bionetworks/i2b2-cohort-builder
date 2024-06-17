library(dplyr)

#' Get parameters from a YAML configuration file
#'
#' @param path path to config file
#' @param active_config The name of the configuration to get parameters from
#'
#' @returns A list of values from the specified configuration
load_config <- function(path, active_config) {
  Sys.setenv(R_CONFIG_ACTIVE = active_config)
  config <- config::get(file = "config.yml")
}

#' Get a list of Participant Identifiers to extract data for from a dataset 
#' that is partitioned by Participant Identifier
#'
#' @param manifest_path path to manifest file containing selected Participant 
#' Identifiers
#' @param dataset_path path to participant-partitioned dataset to extract 
#' participant-partitions from
#'
#' @returns A list containing the unique Participant Identifiers that are in 
#' the manifest list of selected participants and in the source participant-
#' partitioned dataset
get_cohort_partition_paths <- function(manifest_path, dataset_path) {
  f <- read.csv(manifest_path)
  
  participant_ids <- f$PARTICIPANT_ID %>% unique()
  
  dataset <- arrow::open_dataset(dataset_path)
  
  selected_id_dirs <- vector(mode = "character")
  for (x in dataset$files) {
    if (basename(dirname(x)) %in% participant_ids) {
      selected_id_dirs <- 
        selected_id_dirs %>% 
        append(x)
    }
  }
}

#' Extract partitions from a dataset that is partitioned by Participant 
#' Identifier, given a list of paths to Participant Identifier partitions from 
#' the original dataset
#'
#' @param selected_partitions_list A list of paths pointing to dataset partitions
#'
#' @returns An arrow Dataset object
build_cohort <- function(selected_partitions_list) {
  filtered_dataset <- arrow::open_dataset(selected_partitions_list)
}

main <- function() {
  config <- 
    load_config(
      path = "config.yml",
      active_config = "R"
    )
  
  selected_id_dirs <- 
    get_cohort_partition_paths(
      manifest_path = config$participants_csv_path, 
      dataset_path = config$source_dataset_path
    )
  
  filtered_dataset <- 
    build_cohort(
      selected_partitions_list = selected_id_dirs
    )
}

tmp <- main()

