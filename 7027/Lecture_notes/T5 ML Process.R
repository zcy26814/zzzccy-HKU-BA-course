
rm(list=ls()) # Clear environment
cat("\014")   # Clear Console
#dev.off()     # Clear plots

# Set the graphical theme
ggplot2::theme_set(ggplot2::theme_light())
# Set global R options
# The following command disables printing 
# your results in scientific notation.
options(scipen = 999)

library(recipes)  # for feature engineering tasks

# Ames housing data - Load and split
ames <- AmesHousing::make_ames()

set.seed(123)  # for reproducibility
split  <- rsample::initial_split(ames, prop = 0.7, strata = "Sale_Price")
ames_train  <- rsample::training(split)
ames_test   <- rsample::testing(split)


#ames_train_4f = ames_train[c(1:3,57),c('Neighborhood','Gr_Liv_Area','Year_Built','Bldg_Type','Alley','Sale_Price')]
ames_train_4f = ames_train[c(1:4,57),c('Neighborhood','Gr_Liv_Area','Year_Built','Bldg_Type','Alley','Overall_Qual','Sale_Price')]
ames_train_4f = droplevels(ames_train_4f)
ames_train_4f[1,'Year_Built'] = NA
ames_train_4f[1,'Gr_Liv_Area'] = 1000


# Implm one method in ML Process Helper, get simple_blueprint_4f
prepare <- prep(simple_blueprint_4f, training = ames_train_4f)
baked_ames_train_4f <- bake(prepare, new_data = ames_train_4f)

ames_train_4f
baked_ames_train_4f





