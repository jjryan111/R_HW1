library(cluster)
library(ggplot2)
library(tictoc)
library(dplyr)
library(patchwork)

set.seed(42)
sizes <- seq(500, 15000, by = 500)  # Use smaller for example

kmeans_times <- numeric(length(sizes))
kmedoids_times <- numeric(length(sizes))

for (i in seq_along(sizes)) {
  n <- sizes[i]
  
  cluster1 <- data.frame(x = rnorm(n/3, 2, 0.5), y = rnorm(n/3, 2, 0.5))
  cluster2 <- data.frame(x = rnorm(n/3, 6, 0.5), y = rnorm(n/3, 6, 0.5))
  cluster3 <- data.frame(x = rnorm(n/3, 10, 0.5), y = rnorm(n/3, 2, 0.5))
  
  data <- rbind(cluster1, cluster2, cluster3)
  scaled_data <- scale(data)
            
  start_time <- Sys.time()
  kmeans(scaled_data, centers = 3, nstart = 10)
  end_time <- Sys.time()
  kmeans_times[i] <- as.numeric(difftime(end_time, start_time, units = "secs"))

  start_time <- Sys.time()
  pam(scaled_data, 3)
  end_time <- Sys.time()
  kmedoids_times[i] <- as.numeric(difftime(end_time, start_time, units = "secs"))
}


timer_df <- bind_rows(
  data.frame(Size = sizes, Time = kmeans_times, Method = "KMeans"),
  data.frame(Size = sizes, Time = kmedoids_times, Method = "KMedoids")
)

p1 <- ggplot(timer_df, aes(x = Size, y = Time, color = Method)) +
  geom_point(size = 3) +
  geom_line(aes(group = Method), size = 1.2) +
  theme_minimal() +
  ggtitle("Time to Calculate K-Means vs K-Medoids") +
  xlab("Number of Data Points") +
  ylab("Time (seconds)") +
  scale_color_manual(values = c("KMeans" = "blue", "KMedoids" = "red"))


last_data <- data
last_scaled <- scaled_data

last_kmeans <- kmeans(last_scaled, centers = 3, nstart = 10)
last_kmedoids <- pam(last_scaled, 3)

last_data$KMeans_Cluster <- as.factor(last_kmeans$cluster)
last_data$KMedoids_Cluster <- as.factor(last_kmedoids$clustering)
last_data$class <- factor(rep(c("feature_1", "feature_2", "feature_3"), each = n/3))


p2 <- ggplot(last_data, aes(x = x, y = y, color = KMeans_Cluster, shape = class)) +
  geom_point(size = 3) +
  ggtitle("K-Means") +
  theme_minimal()


medoid_points <- last_data[last_kmedoids$id.med, ]
p3 <- ggplot(last_data, aes(x = x, y = y, color = KMedoids_Cluster, shape = class)) +
  geom_point(size = 3) +
  geom_point(data = medoid_points,
             aes(x = x, y = y),
             size = 6, shape = 21, fill = "yellow", color = "black", stroke = 2) +
  ggtitle("K-Medoids") +
  theme_minimal()

print(p1 / p2 / p3)

