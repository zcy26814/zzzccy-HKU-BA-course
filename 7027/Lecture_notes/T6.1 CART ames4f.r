library(rpart)       # direct engine for decision tree application
library(rpart.plot)  # for plotting decision trees

ames <- AmesHousing::make_ames()
summary(ames)

set.seed(123)
split  <- rsample::initial_split(ames, prop = 0.7, strata = "Sale_Price")
ames_train  <- rsample::training(split)

ames_train_sbst = ames_train[,c('Gr_Liv_Area','Lot_Frontage','Lot_Area','Year_Built','Bedroom_AbvGr','Sale_Price')]

## Without specifying any control
ames_dt1_sbst <- rpart(
  formula = Sale_Price ~ .,
  data    = ames_train_sbst,
  method  = "anova"
)
rpart.plot(ames_dt1_sbst)

## control max depth
ames_dt2_sbst <- rpart(
  formula = Sale_Price ~ .,
  data    = ames_train_sbst,
  method  = "anova",
  control = list(maxdepth = 4)
)
rpart.plot(ames_dt2_sbst)

## control min node size
ames_dt3_sbst <- rpart(
  formula = Sale_Price ~ .,
  data    = ames_train_sbst,
  method  = "anova",
  control = list(minbucket = round(0.1*nrow(ames_train_sbst))) # at least 10%
)
rpart.plot(ames_dt3_sbst)


## try to grow the whole tree
ames_dt4_sbst <- rpart(
  formula = Sale_Price ~ .,
  data    = ames_train_sbst,
  method  = "anova",
  control = list(minbucket=1) 
)
rpart.plot(ames_dt4_sbst)




## force grow the whole tree
ames_dt5_sbst <- rpart(
  formula = Sale_Price ~ .,
  data    = ames_train_sbst,
  method  = "anova",
  control = list(minbucket=1,cp=0) 
)
rpart.plot(ames_dt5_sbst)


## get max depth of rpart tree
nodes <- as.numeric(rownames(ames_dt5_sbst$frame))
max(rpart:::tree.depth(nodes))

