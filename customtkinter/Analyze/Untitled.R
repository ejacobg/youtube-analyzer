csv_path <- file.path(getwd(), "New.csv")
data <- read.csv(csv_path)
hist(data$Age)

