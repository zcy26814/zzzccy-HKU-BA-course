
library(FNN) # For func knn
library(gmodels) # For func CrossTable 


# Loading iris dataset
iris.rawData <- iris

# Viewing iris dataset structure and attributes
summary(iris.rawData)

# visualization of data (Optional)
library(ggplot2) # For func ggplot, data visualization
(scatter <- ggplot(iris.rawData, aes(x = Petal.Width, y = Petal.Length, color = Species)) +
    geom_point(size = 2, alpha = 0.5) +
    theme_classic() +
    theme(legend.position = c(0.1, 0.9)))

# normalize data
normalize <- function(x) {
  return ( x - mean(x) )/( sd(x) )
}

# Only normalize the first 4 columns (5th column is label)
iris.normalizeData = iris.rawData
for(i in seq(1,4)){
  iris.normalizeData[,i] = normalize(iris.rawData[,i])
}

# Split into train & test set
set.seed(123)
split  <- rsample::initial_split(iris.normalizeData, prop = 0.7, strata = "Species")
iris.train  <- rsample::training(split)
iris.test   <- rsample::testing(split)
iris.trainFeatMat = iris.train[,1:4]
iris.trainLabel <- iris.train[,5]
iris.testFeatMat <- iris.test[,1:4]
iris.testLabel <- iris.test[,5]

# Building our knn classifier
predictTestLabel <- knn(train = iris.trainFeatMat, test = iris.testFeatMat, cl = iris.trainLabel, k = 3)
Table_PredvsTrue <- data.frame(predictTestLabel, iris.testLabel)
names(Table_PredvsTrue) <- c("Predict", "True")

# inspecting our results table
CrossTable(x = iris.testLabel, y = predictTestLabel, prop.chisq = FALSE)
