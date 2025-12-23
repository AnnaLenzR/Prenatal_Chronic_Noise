# Random sample of 100 from a csv

# Load/install required packages
if (!require("pacman")) install.packages("pacman")
pacman::p_load(dplyr, readr)

# Load data (fix the path: remove ";2D")
dat4 <- read_csv("/Users/annalenz/Library/CloudStorage/OneDrive-UniversityofAlberta/Chronic_noise_rodents/Pre-natal/Pilots/PE_pilot2_anna_5.1/export_be698bfc-d389-4212-9ee1-32c033bf1971_2025-10-22T174405.267992894.csv")

# Set seed for reproducibility (optional)
set.seed(123)

# Take a random sample of 100 unique rows
p100 <- dat4 %>%
  slice_sample(n = 100)

# Check dimensions
dim(p100)

# Save to CSV
write_csv(p100, "/Users/annalenz/Library/CloudStorage/OneDrive-UniversityofAlberta/Chronic_noise_rodents/Pre-natal/Pilots/PE_pilot2_anna_5.1/PCNE_pilot2_100.csv")
