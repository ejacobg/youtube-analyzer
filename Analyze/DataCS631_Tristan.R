# Load required libraries
library(tidyverse)
library(scales)
library(gridExtra)
library(ggplot2)
library(ggpubr)
library(dplyr)
library(tidyr)

degree_path <-  file.path(getwd(), "degree.csv")
top_k_path <- file.path(getwd(), "top_100.csv")
median_data_path <- file.path(getwd(), "median_stats.csv")

degree_data <- read.csv(degree_path)


# Define the binwidth for backlinks
binwidth <- 100

# Calculate the number of rows with a certain number of backlinks
backlinks_counts <- degree_data %>%
  group_by(backlinks = backlinks %/% binwidth) %>%
  summarize(count = n())

# Create the bar graph with scaled x-axis and logarithmic y-axis
p <- ggplot(backlinks_counts, aes(x = backlinks * binwidth, y = count)) +
  geom_bar(stat = "identity", width = binwidth, fill = "#3366FF") + # Set a uniform reddish/pink color for the bars
  xlab("Number of backlinks") +
  ylab("Count") +
  ggtitle("Number of Videos by Backlinks") +
  scale_x_continuous(limits = c(0, 1900), # Change the limits to go up to 1900
                     breaks = seq(0, 1800, binwidth), # Adjust the breaks accordingly
                     expand = c(0.1, 0.1)) +
  scale_y_log10(limits = c(1, 10000))

# Adjust the width of the plot using ggsave()
ggsave("plot.png", p, width = 10, height = 5)


# Get the maximum value for backlinks
max_backlinks <- max(degree_data$backlinks)

# Print the maximum value
cat("The maximum value for backlinks is:", max_backlinks, "\n") 

top_k_data <- read.csv(top_k_path)
category_counts <- top_k_data %>%
  group_by(category) %>%
  summarize(count = n()) %>%
  mutate(percentage = count / sum(count) * 100) %>%
  arrange(desc(percentage))

category_counts$label <- paste(category_counts$category, " (", round(category_counts$percentage, 1), "%)", sep = "")

pie_chart <- ggplot(category_counts, aes(x = "", y = count, fill = factor(label, levels = label))) +
  geom_bar(width = 1, stat = "identity") +
  coord_polar("y", start = 0) +
  theme_minimal() +
  theme(axis.title.x = element_blank(),
        axis.text.x = element_blank(),
        axis.ticks.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks.y = element_blank(),
        legend.title = element_blank()) +
  labs(title = "Pie Chart of Video Categories (Ordered by Percentage)")

# Display the pie chart
print(pie_chart)


box_plot <- ggplot(top_k_data, aes(x = factor(category), y = length)) +
  geom_boxplot() +
  theme_minimal() +
  labs(title = "Box Plot of Video Lengths by Category",
       x = "Category",
       y = "Length (seconds)") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Display the box plot
print(box_plot)

# Code for average/median trends

# Load CSV data
median_avg_data <- read.csv(median_data_path)

# Reshape the data to make it suitable for creating box plots
data_long <- median_avg_data %>%
  gather(key = "metric", value = "value", -category)
# Create a bar chart function for the desired formatting
create_bar_chart <- function(data, metric_title) {
  plot <- ggplot(data, aes(x = factor(category), y = value, fill = factor(category))) +
    geom_bar(stat = "identity") +
    theme_minimal() +
    labs(title = paste("Bar Chart of", metric_title, "by Category"),
         x = "Category") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1),
          axis.title.y = element_blank(),
          legend.position = "none")
  return(plot)
}

# Create and display bar charts for each metric
average_length_plot <- create_bar_chart(data_long %>% filter(metric == "average_length"), "Average Length")
average_views_plot <- create_bar_chart(data_long %>% filter(metric == "average_views"), "Average Views")
median_length_plot <- create_bar_chart(data_long %>% filter(metric == "median_length"), "Median Length")
median_views_plot <- create_bar_chart(data_long %>% filter(metric == "median_views"), "Median Views")

print(average_length_plot)
print(average_views_plot)
print(median_length_plot)
print(median_views_plot)