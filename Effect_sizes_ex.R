# Pilot extraction Prenatal chronic noise 

## Install / Load packages using pacman
if (!require("pacman")) install.packages("pacman")
pacman::p_load(tidyverse, 
               metaDigitise,
               devtools,
               plyr)

# My directory
fig_dir <- "/Users/annalenz/Desktop/ChronicNoise_Rodents/Figs"


## Call data
data <- metaDigitise(dir = "/Users/annalenz/Desktop/ChronicNoise_Rodents/Figs")

## Extract the data we collected from the images
dat <- getExtracted("/Users/annalenz/Desktop/ChronicNoise_Rodents/Figs", summary = TRUE)


## Save as CSV
write.csv(
  dat,
  file = file.path(fig_dir, "metaDigitise_output.csv"),
  row.names = FALSE
)
›